from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
import schema, models

router = APIRouter(prefix="/books", tags=["Books"])

# -----------------------------------------SEARCH BOOK-----------------------------------------
@router.get("/search/")
def book_search(title: str, db:Session=Depends(get_db)):
    books = db.query(models.Books).filter(models.Books.title.contains(title)).all()
    if not books:
        raise HTTPException(status_code=404, detail="No books found")
    return books

# -----------------------------------------CREATE BOOK-----------------------------------------
@router.post("/", response_model=schema.Book)
def book_create(book: schema.BookCreate, db: Session = Depends(get_db)):
    # Step 1: Validate user_id
    users = db.query(models.Users).filter(models.Users.id == book.user_id).first()
    if not users:
        raise HTTPException(status_code=400, detail = "Invalid user_id")

    # Step 2: Check duplicate book
    existing_book = db.query(models.Books).filter(models.Books.title == book.title, models.Books.user_id == book.user_id).first()
    if existing_book:
        raise HTTPException(status_code=400, detail="Book already exists for this user")
        
    # Step 3: Create book
    new_book = models.Books(
        title = book.title,
        author = book.author,
        user_id = book.user_id
    )

    # Save book in database
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book     # Return created book

# -----------------------------------------GET ALL BOOK-----------------------------------------
@router.get("/", response_model=list[schema.Book])               # Get list of books
def books_get(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Books).offset(skip).limit(limit).all()               # Example: skip=0 → start from beginning; limit=10 → show only 10 users

# -----------------------------------------GET BOOK BY ID-----------------------------------------
@router.get("/{book_id}", response_model=schema.Book)
def book_get_by_id(book_id: int, db: Session = Depends(get_db)):
    # Step 1: Find book
    existing_book = db.query(models.Books).filter(models.Books.id == book_id).first()
    # If not found → error
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book ID not found")
        
    return existing_book        # Return book

# -----------------------------------------BOOK WITH USER DETAILS-----------------------------------------
@router.get("/book-with-user/{book_id}", response_model=schema.BookWithUser)    
def book_with_user_get(book_id : int, db: Session = Depends(get_db)):       # Get book + its owner details
    # Step 1: Find book id
    existing_book = db.query(models.Books).filter(models.Books.id == book_id).first()
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book Not Found")
    return existing_book        # Return book
    
# -----------------------------------------UPDATE BOOK-----------------------------------------
@router.put("/{book_id}", response_model=schema.BookWithUser)
def book_update(book_id:int, book : schema.BookCreate, db: Session = Depends(get_db)):
    # Step 1: Find book
    db_book = db.query(models.Books).filter(models.Books.id==book_id).first()
    # If not found → error
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Step 2: Check user exists
    user = db.query(models.Users).filter(models.Users.id == book.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user_id")

    # Update book values
    db_book.title = book.title
    db_book.author = book.author
    db_book.user_id = book.user_id

    db.commit()
    db.refresh(db_book)

    return db_book
    
# -----------------------------------------DELETE BOOK-----------------------------------------
@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session= Depends(get_db)):
    # Step 1: Find book
    db_book = db.query(models.Books).filter(models.Books.id == book_id).first()
    # If not found → error
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Delete book from database 
    db.delete(db_book)
    db.commit()

    return {"message" : "Book deleted"}


