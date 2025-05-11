from fastapi import APIRouter
from app.services.grocery_service import fetch_grocery_prices, save_grocery_price, fetch_grocery_price, update_grocery_price, delete_grocery_price
#         # Delete the grocery price data from DynamoDB
from app.models.price import GroceryPriceResponse, GroceryPriceRequest

router = APIRouter(
    prefix="/grocery-prices",
    tags=["Grocery Prices"]
)

@router.get("/", response_model=GroceryPriceResponse)
async def get_grocery_prices():
    return await fetch_grocery_prices()

@router.get("/{uid}", response_model=GroceryPriceResponse)
async def get_grocery_prices(uid: str):
    return await fetch_grocery_price(uid)

@router.post("/", status_code=201)
async def post_grocery_prices(price_data: GroceryPriceRequest):
    return await save_grocery_price(price_data)

@router.patch("/{uid}", status_code=200)
async def save_grocery_prices(uid: str, price_data: GroceryPriceRequest):
    return await update_grocery_price(uid, price_data)

@router.delete("/{uid}", status_code=200)
async def remove_grocery_prices(uid: str):
    return await delete_grocery_price(uid)
