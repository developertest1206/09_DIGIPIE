# Import required tools
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

# This is a built-in form for handling token input (Authorization header)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials     
 
# Import database, models and schema
import models, schema
from db import get_db

# Import token verification function
from auth import verify_token


# Create router for item APIs. All APIs will start with /item and will be taged as "Items" in documentation
router = APIRouter(prefix="/item", tags=["Items"])



# -------- GET CURRENT USER --------
# This line creates a security system that will read token from request header
# It expects data in this format: Authorization: Bearer <token>
security = HTTPBearer()

# This function is used to check if the user is logged in or not
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials     # Get the actual token value (remove "Bearer" word automatically)
    payload = verify_token(token)       # Check if token is valid (not fake, not expired)

    if payload is None:
        # If token is wrong or expired, stop user and show error
        raise HTTPException(status_code=401, detail="Invalid Token")

    return payload          # If token is correct, return user data (payload)


# -------- CREATE ITEM --------
# Only logged-in user can create item
@router.post("/")
def item_createe(
    item: schema.ItemCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)   # check login
):
    # Create new item
    new_item = models.Items(title=item.title)

    # Save item in database
    db.add(new_item)
    db.commit()
    
    return {"message": "Item created"}



# -------- GET ALL ITEMS --------
# Only logged-in user can see items
@router.get("/", response_model=list[schema.Item])
def items_get(db: Session = Depends(get_db)):
    return db.query(models.Items).all()     # Get all items from database




# -------- DELETE ITEM --------
# Only logged-in user can delete item
@router.delete("/{item_id}")
def item_delete(
    item_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)   # check login
):
    # Find item by ID
    item = db.query(models.Items).filter(models.Items.id == item_id).first()

    # If item not found -> show error
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Delete item
    db.delete(item)
    db.commit()

    return {"message": "Deleted"}