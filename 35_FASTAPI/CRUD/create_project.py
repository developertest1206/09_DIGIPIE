import os

# 👉 Target project folder
base_path = "../01_PROJECT"   # go outside CRUD → into 01_PROJECT

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