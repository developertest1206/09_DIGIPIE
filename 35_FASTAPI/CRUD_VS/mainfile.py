from fastapi import FastAPI, HTTPException, Form, UploadFile, File      # FastAPI tools to create API and handle file upload
from fastapi.responses import FileResponse               # Import FileResponse to send file back to user
import os         # os to work with folder and file paths
app= FastAPI()     # Create FastAPI app

from typing import List, Annotated


# Create a folder named "mainfile" to store uploaded files. 
UPLOAD_FOLDER = "mainfile"

# If the folder already exists, do nothing (no error). If folder does not exist, create it
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



# -------------------- GET STRING --------------------
# Simple test API. When you open http://127.0.0.1:8000/ in browser, it will show this message
@app.get("/")
def home_get():
    return {"message" : "Welcome to FastAPI!"}


# -------------------- UPLOAD SINGLE FILE --------------------
@app.post("/upload")
# file: UploadFile means user will upload a file. File(...) means file is required
async def upload_file(file: UploadFile= File(...)):

    # Create full file path (folder + file name) (example: uploads/file.png)
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # If file is already present in folder, stop and return error
    if os.path.exists(file_path):
        raise HTTPException(status_code=400, detail="File already exists")


    # Open file in write mode (wb = write binary) and Save file into folder
    with open(file_path, "wb") as f:
        while chunk := await file.read(1024):
            f.write(chunk)

    # Send response back to user
    return {
        "message": "File Upload successfully",
        "file_name": file.filename,
        "content_type": file.content_type     # Type of file (example: image/png, text/plain)
    }


# -------------------- GET ALL FILE NAMES --------------------
@app.get("/files")
def list_files():
    
    # Get all files from uploads folder
    files = os.listdir(UPLOAD_FOLDER)

    return {
        "files": files
    }


# -------------------- DOWNLOAD FILE --------------------
@app.get("/download/{filename}")
def download_file(filename: str):
    
    # Create full path
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    # Check if file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Send file to user
    return FileResponse(path=file_path, filename=filename)


# -------------------- DELETE FILE --------------------
@app.delete("/delete/{filename}")
def delete_file(filename: str):
    
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    # Check if file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Delete file
    os.remove(file_path)

    return {
        "message": "File deleted successfully",
        "file_name": filename
    }


# -------------------- FILE INFO --------------------
@app.get("/file-info/{filename}")
# This API does not save file, only shows information
def file_info(filename: str):

    file_path = os.path.join(UPLOAD_FOLDER, filename)

    # Check if file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Get file size
    size = os.path.getsize(file_path)

    return {
        "file_name": filename,      # Name of file with example: image/png, text/plain
        "file_size_bytes": size,     # Size of file
    }









# # -------------------- UPLOAD MULTIPLE FILES --------------------
@app.post("/upload-multiple")
# files: list means user can upload multiple files at once
async def upload_multiple(files: list[UploadFile] = File(...)):

    # List to store saved file names
    saved_files = []

    for file in files:
        # Create file path for each file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        # Open file and save it
        with open(file_path, "wb") as f:
            while chunk := await file.read(1024):
                f.write(chunk)

        saved_files.append(file.filename)   # Save file name in list

        # IMPORTANT: return should be outside loop (after all files saved)
    return {
        "message" : "Multiple files uploaded",
        "files" : saved_files
    }