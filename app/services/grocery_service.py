import boto3
from botocore.exceptions import ClientError
from decimal import Decimal
import random
from app.models.price import GroceryPriceRequest, GroceryPriceResponse, GroceryPrice

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table_name = 'food-prices'
table = dynamodb.Table(table_name)

async def save_grocery_price(price_data: GroceryPriceRequest):
    try:
        # Generate a unique identifier using random numbers
        uid = str(random.randint(10000000, 99999999))
        while table.get_item(Key={'uid': uid}).get('Item'):
            uid = str(random.randint(10000000, 99999999))

        # Save the grocery price data to DynamoDB
        table.put_item(
            Item={
                'uid': uid,
                'store_name': price_data.store_name,
                'item_name': price_data.item_name,
                'price': Decimal(str(price_data.price)),
                'zip_code': price_data.zip_code
            }
        )
        
        return {"message": "Price data saved successfully."}
    except ClientError as e:
        return {"error": f"Failed to save price data: {e.response['Error']['Message']}"}
    
async def fetch_grocery_prices():

    try:
        response = table.scan()
        items: list[GroceryPrice] = response.get('Items', [])
        
        grocery_prices = GroceryPriceResponse(items=items)

        return grocery_prices
    except ClientError as e:
        return {"error": f"Failed to fetch price data: {e.response['Error']['Message']}"}

async def fetch_grocery_price(uid: str):
    try:
        response = table.get_item(Key={'uid': uid})
        item = response.get('Item')

        if not item:
            return {"error": "Price data not found."}

        grocery_price = GroceryPriceResponse(items=[GroceryPrice(**item)])

        return grocery_price
    except ClientError as e:
        return {"error": f"Failed to fetch price data: {e.response['Error']['Message']}"}
    
async def update_grocery_price(uid: str, price_data: GroceryPriceRequest):
    try:
        # Update the grocery price data in DynamoDB
        table.update_item(
            Key={'uid': uid},
            UpdateExpression="SET store_name = :store_name, item_name = :item_name, price = :price, zip_code = :zip_code",
            ExpressionAttributeValues={
                ':store_name': price_data.store_name,
                ':item_name': price_data.item_name,
                ':price': Decimal(str(price_data.price)),
                ':zip_code': price_data.zip_code
            }
        )
        
        return {"message": "Price data updated successfully."}
    except ClientError as e:
        return {"error": f"Failed to update price data: {e.response['Error']['Message']}"}

async def delete_grocery_price(uid: str):
    try:
        # Delete the grocery price data from DynamoDB
        table.delete_item(Key={'uid': uid})

        return {"message": "Price data deleted successfully."}
    except ClientError as e:
        return {"error": f"Failed to delete price data: {e.response['Error']['Message']}"}




    

    
