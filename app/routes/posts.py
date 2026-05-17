from fastapi import APIRouter
from app.services.github_service import get_user

router = APIRouter()

@router.get("/weekly")
async def weekly_posts():
    return {
        "posts": []
    }

@router.get("/github-test")
async def github_test():
    return await get_user()