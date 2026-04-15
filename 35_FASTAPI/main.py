from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get_product():
    return {
        "laptop" : "Macbook Pro 16 inch",
        "phone" : "iphone 14 Pro Max"
            }

@app.get("/product/{product_id}")
def get_product_by_id(product_id : int):
    return {"id" : product_id}


