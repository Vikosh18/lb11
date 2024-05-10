from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# Імпровізована база даних для зберігання постів
posts_db = {
    1: {"title": "Post 1", "content": "Content of post 1"},
    2: {"title": "Post 2", "content": "Content of post 2"},
    3: {"title": "Post 3", "content": "Content of post 3"}
}

# Модель для валідації посту
class Post(BaseModel):
    title: str
    content: str

# Модель для валідації статистики
class Stats(BaseModel):
    version: int = 0
    posts: int = 0
    stats: int = 0

# Маршрутизатор для версії
@app.get("/version", tags=["version"])
def get_version(request: Request):
    request.app.state.version_counter += 1
    return {"version": "1.0"}

# Маршрутизатор для постів
posts_router = FastAPI()

@posts_router.post("/posts", tags=["posts"])
def create_post(post: Post, request: Request):
    request.app.state.posts_counter += 1
    post_id = max(posts_db.keys()) + 1
    posts_db[post_id] = post.dict()
    return {"message": "Post created successfully", "post_id": post_id}

@posts_router.put("/posts/{post_id}", tags=["posts"])
def update_post(post_id: int, post: Post, request: Request):
    request.app.state.posts_counter += 1
    if post_id not in posts_db:
        raise HTTPException(status_code=404, detail="Post not found")
    posts_db[post_id] = post.dict()
    return {"message": "Post updated successfully"}

@posts_router.delete("/posts/{post_id}", tags=["posts"])
def delete_post(post_id: int, request: Request):
    request.app.state.posts_counter += 1
    if post_id not in posts_db:
        raise HTTPException(status_code=404, detail="Post not found")
    del posts_db[post_id]
    return {"message": "Post deleted successfully"}

app.mount("/posts", posts_router)

# Маршрутизатор для статистики
@app.get("/stats", tags=["stats"])
def get_stats(request: Request):
    request.app.state.stats_counter += 1
    version_counter = request.app.state.version_counter
    posts_counter = request.app.state.posts_counter
    stats_counter = request.app.state.stats_counter
    return {
        "version": version_counter,
        "posts": posts_counter,
        "stats": stats_counter
    }

if __name__ == "__main__":
    import uvicorn
    app.state.version_counter = 0
    app.state.posts_counter = 0
    app.state.stats_counter = 0
    uvicorn.run(app, host="127.0.0.1", port=8000)
