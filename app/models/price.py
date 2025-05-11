from pydantic import BaseModel
from typing import List

class GroceryPrice(BaseModel):
    uid: str
    store_name: str
    item_name: str
    price: float
    zip_code: str

class GroceryPriceResponse(BaseModel):
    items: List[GroceryPrice]

class GroceryPriceRequest(BaseModel):
    store_name: str
    item_name: str
    price: float
    zip_code: str
