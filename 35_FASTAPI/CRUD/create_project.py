import os

# 👉 Target project folder
base_path = "D:/09_DIGIPIE/35_FASTAPI/02_CRUD_POSTGRESQL"   # go outside CRUD → into 

folders = [
    "crud",
    "routers"
]

files = [
    "main.py",
    "database.py",
    "models.py",
    "schemas.py",
    "crud/user.py",
    "routers/user.py"
]

# ------------------------------
# Create base project folder
# ------------------------------
os.makedirs(base_path, exist_ok=True)

# ------------------------------
# Create folders inside base_path
# ------------------------------
for folder in folders:
    os.makedirs(os.path.join(base_path, folder), exist_ok=True)

# ------------------------------
# Create files inside base_path
# ------------------------------
for file in files:
    file_path = os.path.join(base_path, file)

    # Create parent folder if needed
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as f:
        pass

print("✅ Project created inside 01_PROJECT folder!")