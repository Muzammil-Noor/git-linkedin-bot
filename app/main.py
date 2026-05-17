from fastapi import FastAPI
from app.routes.posts import router as posts_router

app = FastAPI()

app.include_router(posts_router, prefix="/posts")

@app.get("/")
async def root():
    return {"message": "Git LinkedIn Bot running"}