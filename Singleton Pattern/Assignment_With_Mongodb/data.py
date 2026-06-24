from pymongo import MongoClient

URL = "mongodb+srv://single:single123@cluster0.wkza9aw.mongodb.net/?appName=Cluster0"

client = MongoClient(URL)

db = client["singleton_db"]
collection = db["Users"]

# Remove old data
collection.delete_many({})

users = [
    {
        "student_id": "CSE22001",
        "name": "Jubayer Ahmed Sojib",
        "email": "jubayer.cse@du.ac.bd",
        "role": "Project Leader",
        "department": "Computer Science and Engineering"
    },
    {
        "student_id": "CSE22002",
        "name": "Tanvir Hasan",
        "email": "tanvir.cse@du.ac.bd",
        "role": "Backend Developer",
        "department": "Computer Science and Engineering"
    },
    {
        "student_id": "CSE22003",
        "name": "Fahim Ahmed",
        "email": "fahim.cse@du.ac.bd",
        "role": "Database Administrator",
        "department": "Computer Science and Engineering"
    },
    {
        "student_id": "CSE22004",
        "name": "Mahadi Hasan",
        "email": "mahadi.cse@du.ac.bd",
        "role": "Frontend Developer",
        "department": "Computer Science and Engineering"
    },
    {
        "student_id": "CSE22005",
        "name": "Sakib Hossain",
        "email": "sakib.cse@du.ac.bd",
        "role": "Software Tester",
        "department": "Computer Science and Engineering"
    },
    {
        "student_id": "CSE22006",
        "name": "Nafis Rahman",
        "email": "nafis.cse@du.ac.bd",
        "role": "UI/UX Designer",
        "department": "Computer Science and Engineering"
    },
    {
        "student_id": "CSE22007",
        "name": "Rifat Islam",
        "email": "rifat.cse@du.ac.bd",
        "role": "DevOps Engineer",
        "department": "Computer Science and Engineering"
    },
    {
        "student_id": "CSE22008",
        "name": "Muntasir Ahmed",
        "email": "muntasir.cse@du.ac.bd",
        "role": "AI Engineer",
        "department": "Computer Science and Engineering"
    }
]

result = collection.insert_many(users)

print("=" * 50)
print("MongoDB Seed Successful")
print("=" * 50)
print(f"Inserted Users: {len(result.inserted_ids)}")

for user in users:
    print(f"✓ {user['name']} - {user['role']}")

client.close()