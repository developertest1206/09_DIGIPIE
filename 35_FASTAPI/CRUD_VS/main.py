from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Hello World!"}

@app.get("/users")
def get_users(name: str):
    return {"name": name}