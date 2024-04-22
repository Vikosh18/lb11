from fastapi import FastAPI, HTTPException, Path, Query, Body, Depends, APIRouter
from typing import Optional, List, Dict
from pydantic import BaseModel

# Клас-модель для постів
class Post(BaseModel):
    id: int
    title: str
    content: str

# Створення FastAPI додатку
app = FastAPI()

# Створення маршрутизаторів для кожної кінцевої точки
version_router = APIRouter()
posts_router = APIRouter()
stats_router = APIRouter()

# Створення імпровізованої бази даних - словника в пам'яті
posts_db: Dict[int, Post] = {
    1: Post(id=1, title="First Post", content="Content of the first post"),
    2: Post(id=2, title="Second Post", content="Content of the second post"),
}

# Кінцева точка "version"
@version_router.get("/version")
async def version():
    return {"version": "1.0"}

# Кінцева точка "posts"
@posts_router.get("/posts/{post_id}")
async def read_post(post_id: int):
    if post_id not in posts_db:
        raise HTTPException(status_code=404, detail="Post not found")
    return posts_db[post_id]

@posts_router.post("/posts")
async def create_post(post: Post):
    posts_db[post.id] = post
    return post

@posts_router.put("/posts/{post_id}")
async def update_post(post_id: int, post: Post):
    if post_id not in posts_db:
        raise HTTPException(status_code=404, detail="Post not found")
    posts_db[post_id] = post
    return post

@posts_router.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    if post_id not in posts_db:
        raise HTTPException(status_code=404, detail="Post not found")
    deleted_post = posts_db.pop(post_id)
    return deleted_post

# Кінцева точка "stats"
@stats_router.get("/stats")
async def stats():
    return {"stats": "Statistics data"}

# Додавання маршрутизаторів до FastAPI додатку
app.include_router(version_router, prefix="/api")
app.include_router(posts_router, prefix="/api")
app.include_router(stats_router, prefix="/api")
