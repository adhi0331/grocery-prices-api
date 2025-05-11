# main.py
from fastapi import FastAPI
from app.routers import prices

app = FastAPI()

# Register the router
app.include_router(prices.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Price API!"}

