from fastapi import FastAPI     # Import FastAPI framework (used to create APIs)
 
app = FastAPI()     # Create FastAPI app (instance of FastAPI class)

@app.get("/")           # This API runs when user opens: http://127.0.0.1:8000/
def get_product():
    # Return simple product data (dictionary)
    return {
        "laptop": "Macbook Pro 16 inch",
        "phone": "iphone 14 Pro Max"
    }

# This API runs when user opens: http://127.0.0.1:8000/product/1
@app.get("/product/{product_id}")
def get_product_by_id(product_id: int):
    # product_id is taken from URL
    # Example: /product/5 → product_id = 5

    # Return product id
    return {"id": product_id}