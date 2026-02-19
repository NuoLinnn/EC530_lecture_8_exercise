from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/")
async def get_food_data():
    external_url = "https://api.fda.gov/food/enforcement.json?search=report_date:[20040101+TO+20131231]&limit=1"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(external_url)
            response.raise_for_status()
            return response.json()
    
    except httpx.RequestError as e:
        print(f"Error: idk what to put here")