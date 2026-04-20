from fastapi import Form
from fastapi.params import Depends
from fastapi.responses import RedirectResponse
from requests import Session
from sqlalchemy import text
from websockets.asyncio import router

from database import get_db


# ------------------------------
# INSERT USER
# ------------------------------
@router.post("/")
def create_user(
        name: str = Form(...),
        email: str = Form(...),
        age: int = Form(...),
        db: Session = Depends(get_db)
):
    query = text("INSERT INTO "b_users" (name, email, age) VALUES (:name, :email, :age)")

    db.execute(query, {
        "name": name,
        "email": email,
        "age": age
    })

    db.commit()

    # Redirect back to home page
    return RedirectResponse(url="/", status_code=303)