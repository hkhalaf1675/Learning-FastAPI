from fastapi import FastAPI, HTTPException
import math
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

class ResponseModel(BaseModel):
    success: bool
    data: dict

class ProductCategory(str, Enum):
    computer_and_laptops = "Computer and Laptops"
    bags = "Bags"

class ProductModel(BaseModel):
    id: int | None
    name: str
    category: ProductCategory
    price: float
    stock: int

# mock data
products = [
    {"id": 1, "category": "Computer and Laptops", "name": "Wireless Mouse", "price": 24.99, "stock": 45},
    {"id": 2, "category": "Computer and Laptops", "name": "Mechanical Keyboard", "price": 89.99, "stock": 22},
    {"id": 3, "category": "Computer and Laptops", "name": "Bluetooth Headphones", "price": 59.95, "stock": 15},
    {"id": 4, "category": "Computer and Laptops", "name": "USB-C Cable", "price": 12.50, "stock": 120},
    {"id": 5, "category": "Computer and Laptops", "name": "External SSD 1TB", "price": 129.99, "stock": 0},
    {"id": 6, "category": "Computer and Laptops", "name": "Smartphone Stand", "price": 9.99, "stock": 65},
    {"id": 7, "category": "Computer and Laptops", "name": "Wireless Charger", "price": 29.95, "stock": 30},
    {"id": 8, "category": "Computer and Laptops", "name": "Laptop Backpack", "price": 49.99, "stock": 18},
    {"id": 9, "category": "Computer and Laptops", "name": "Noise Cancelling Earbuds", "price": 149.99, "stock": 12},
    {"id": 10, "category": "Computer and Laptops", "name": "Ergonomic Mouse Pad", "price": 14.99, "stock": 85},
    {"id": 11, "category": "Computer and Laptops", "name": "HD Webcam", "price": 79.50, "stock": 10},
    {"id": 12, "category": "Computer and Laptops", "name": "Portable Power Bank", "price": 34.99, "stock": 0}
]

@app.get("/products/{product_id}", response_model=ResponseModel)
async def get_product_by_id(product_id: int):
    product = next((item for item in products if item["id"] == product_id), None)
    
    if product:
        return {
            "success": True,
            "data": {
                "product": product
            }
        }
    else:
        raise HTTPException(status_code=404, detail={
            "success": False,
            "message": "Validation Error",
            "errors": ["There is no product with this id"]
        })
    
@app.get("/products", response_model=ResponseModel)
async def get_products(page: int = 1, limit: int = 10, maxPrice: float | None = None, exists: bool | None = None):
    filtered_products = products.copy()
    if maxPrice:
        filtered_products = list(filter(lambda p: p["price"] <= maxPrice, filtered_products))
    elif exists:
        filtered_products = list(filter(lambda p: p["stock"] > 0, filtered_products))

    return {
        "success": True,
        "data": {
            "pageInfo": {
                "currentPage": page,
                "totalPages": math.ceil(len(filtered_products) / limit),
                "totalItems": len(filtered_products)
            },
            "products": filtered_products[((page - 1) * limit): (page * limit)]
        }
    }

@app.post("/products", response_model=ResponseModel, status_code=201)
async def create_product(product: ProductModel):
    product.id = len(products) + 1
    products.append(product)

    response: ResponseModel = {
        "success": True,
        "data": {
            "product": products[len(products) - 1]
        }
    }
    return response