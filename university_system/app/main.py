from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import get_database
from app.routers import auth, classroom, notice

app = FastAPI(title="University Management System")

# Configure CORS Middleware to allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],  # Add the URL/port your frontend is running on (or "*" for open dev access)
    allow_credentials=True,
    allow_methods=["*"],  # Allows OPTIONS, GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Allows Authorization, Content-Type, etc.
)

app.include_router(auth.router)
app.include_router(classroom.router)
app.include_router(notice.router)


@app.on_event("startup")
def startup_event():
    get_database()  # triggers the Singleton connection exactly once
    print("University Management System started.")


@app.get("/")
def root():
    return {"message": "University Management System API is running"}