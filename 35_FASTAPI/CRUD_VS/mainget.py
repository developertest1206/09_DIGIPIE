from fastapi import FastAPI     # FastAPI is used to create APIs

application = FastAPI()     # Create main app instance (entry point of your API)

# This API runs when user opens: http://127.0.0.1:8000/
@application.get("/")
def get_product():
    # Return simple data in dictionary format (JSON response)
    return {
        "laptop": "Macbook Pro 16 inch",
        "phone": "iphone 14 Pro Max"
    }


# This API runs when user opens: http://127.0.0.1:8000/product/1
@application.get("/product/{product_id}")
def get_product_by_id(product_id: int):
    # product_id is a PATH PARAMETER (value comes from URL)

    # Example:
    # /product/5 → product_id = 5

    # Return product id in response
    return {"id": product_id}


# This API runs when user opens: http://127.0.0.1:8000/products/1?q=search_term
@application.get("/products/{product_id}")
def get_product_by_id_and_query(product_id: int, q: str = None):
    # product_id → comes from URL (path parameter)
    # q → comes from query parameter (after ? in URL)

    # Example:
    # /products/5?q=mobile → product_id = 5, q = "mobile"

    return {
        "id": product_id,
        "query": q
    }


# This API runs when user opens: http://127.0.0.1:8000/products?skip=5&limit=20
@application.get("/products")
def get_products(skip: int = 0, limit: int = 10):
    # skip and limit are QUERY PARAMETERS

    # Example:
    # /products?skip=5&limit=20 → skip = 5, limit = 20

    # These are commonly used for pagination (loading data in parts)

    return {
        "skip": skip,
        "limit": limit
    }