import uuid
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from app.models import RegisterRequest, LoginRequest
from app.database import get_database
from app.factories.user_factory import UserFactory
from app.auth_utils import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/register")
def register(request: RegisterRequest):
    db = get_database()
    if db.users.find_one({"email": request.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    user_id = str(uuid.uuid4())

    # --- Factory Pattern ---
    # This endpoint never imports Student/Teacher/Admin directly; it
    # just asks the factory for "whatever role was requested".
    try:
        user_obj = UserFactory.create_user(
            role=request.role, user_id=user_id, name=request.name, email=request.email
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    db.users.insert_one(
        {
            "user_id": user_id,
            "name": request.name,
            "email": request.email,
            "password": hash_password(request.password),
            "role": user_obj.get_role(),
        }
    )
    return {"message": "User registered", "user_id": user_id, "role": user_obj.get_role()}


@router.post("/login")
def login(request: LoginRequest):
    db = get_database()
    user = db.users.find_one({"email": request.email})
    if not user or not verify_password(request.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user["user_id"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer", "role": user["role"], "user_id": user["user_id"]}


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    db = get_database()
    user = db.users.find_one({"user_id": payload["sub"]})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def require_role(*allowed_roles):
    """Dependency factory for simple role-based route protection."""
    def role_checker(user=Depends(get_current_user)):
        if user["role"] not in allowed_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return role_checker
