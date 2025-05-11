import httpx
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Function to find grocery stores near a given zip code:
async def find_nearby_stores(zip_code: str, distance: int = 10):
    
    # Get the latitude and longitude of the zip code using Google Maps API
    async with httpx.AsyncClient() as client:
        print(GOOGLE_API_KEY)
        geo_resp = await client.get(
            "https://maps.googleapis.com/maps/api/geocode/json",
            params={
                "address": zip_code,
                "key": GOOGLE_API_KEY
            }
        )
        geo_data = geo_resp.json()
        print(geo_data)
        if geo_data["status"] != "OK":
            return {"error": "Invalid zip code or address."}
        
        location = geo_data["results"][0]["geometry"]["location"]
        lat = location["lat"]
        lng = location["lng"]
    
    ## Find nearby grocery stores using Google Places API
    async with httpx.AsyncClient() as client:
        places_resp = await client.get(
            "https://maps.googleapis.com/maps/api/place/nearbysearch/json",
            params={
                "location": f"{lat},{lng}",
                "radius": distance * 1609.34,  # Convert miles to meters
                "type": "grocery_or_supermarket",
                "key": GOOGLE_API_KEY
            }
        )
        places_data = places_resp.json()
        if places_data["status"] != "OK":
            return {"error": "Failed to fetch nearby stores."}
        
        stores = []
        for place in places_data["results"]:
            stores.append({
                "name": place["name"],
                "address": place["vicinity"]
            })
    
    return stores