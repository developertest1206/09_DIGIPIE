from fastapi import FastAPI         # Import FastAPI framework (used to create APIs)
from pydantic import BaseModel      # Import BaseModel (used for data validation)
from typing import List             # Import List type (to store multiple items)

# ----------------------------------
# Create FastAPI app
# ----------------------------------
app = FastAPI()

# ----------------------------------
# Create a data model for Tea (structure of tea data)
# ----------------------------------
class Tea(BaseModel):
    id: int       # Unique ID of tea
    name: str     # Name of tea
    origin: str   # Country/Place of origin

# ----------------------------------
# Create an empty list to store teas (acts like database)
# ----------------------------------
teas: List[Tea] = []

# ----------------------------------
# Root endpoint (just to check API is working)
# ----------------------------------
@app.get("/")
def read_root():
    return {"message": "Welcome to the Tea API!"}

# ----------------------------------
# GET all teas
# ----------------------------------
@app.get("/teas")
def get_teas():
    return teas   # Return all teas from list

# POST - Add new tea
@app.post("/teas")
def add_teas(tea: Tea):
    teas.append(tea)   # Add tea to list
    return tea         # Return added tea

# ----------------------------------
# PUT - Update tea using ID
# ----------------------------------
@app.put("/teas/{tea_id}")
def update_tea(tea_id: int, updated_tea: Tea):
    # Loop through teas list
    for index, tea in enumerate(teas):
        # Check if ID matches
        if tea.id == tea_id:
            teas[index] = updated_tea   # Replace old tea with new data
            return updated_tea          # Return updated tea
    
    # If tea not found
    return {"error": "Tea not found"}

# ----------------------------------
# DELETE - Remove tea using ID
# ----------------------------------
@app.delete("/teas/{tea_id}")
def delete_tea(tea_id: int):
    # Loop through teas list
    for index, tea in enumerate(teas):
        # Check if ID matches
        if tea.id == tea_id:
            deleted = teas.pop(index)   # Remove tea from list
            return deleted             # Return deleted tea
    
    # If tea not found
    return {"error": "Tea not found."}