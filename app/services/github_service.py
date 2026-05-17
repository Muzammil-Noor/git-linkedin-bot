import httpx
from app.config import GITHUB_TOKEN

BASE_URL = "https://api.github.com"

async def get_user():
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/user",
            headers=headers
        )

    return response.json()