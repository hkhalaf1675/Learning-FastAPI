from fastapi import FastAPI

app = FastAPI()

# root endpoint
@app.get("/")
async def root():
    return { "message": "Hello World, From FastAPI P01" }

# Post Apis
posts = [
    {"id": 0, "title": "post num 0", "content": "post content"},
    {"id": 1, "title": "post num 1", "content": "post content"},
    {"id": 2, "title": "post num 2", "content": "post content"},
    {"id": 3, "title": "post num 3", "content": "post content"},
]
@app.get("/posts", description="get all posts")
async def get_posts():
    return {
        "message": "get all posts",
        "data": {
            "posts": posts
        },
        "code": 200
    }
@app.get("/posts/{id}", description="get one post by it's id", deprecated=True)
async def get_post(id: int):
    for post in posts:
        if post.id == id:
            return {
                "message": "get post successfully",
                "data": {
                    "post": post
                },
                "code": 200
            }
    return {
        "message": "there is no post exists with this id",
        "data": {
            "post": None
        },
        "code": 404
    }
@app.post("/posts", description="create new post")
async def create_post(title, content):
    id = len(posts)
    post = {
        "id": id,
        "title": title,
        "content": content
    }
    posts.append(post)

    return {
        "message": "Post has been added successfully",
        "data": {
            "post": posts[id]
        },
        "code": 200
    }
@app.put("/posts/{id}", description="update specific post", deprecated=True)
async def update_post(id: int, title: str, content: str):
    for post in posts:
        if post.id == id:
            post.title = title
            post.content = content

            return {
                "message": "Post has been updated successfully",
                "data": {},
                "code": 200
            }
    return {
        "message": "there is no post exists with this id",
        "data": {},
        "code": 404
    }
@app.delete("/posts/{id}", description="delete post")
async def delete_post(id: int):
    for post in posts:
        if post.id == id:
            posts.remove(post)
            return {
                "message": "Post has been deleted successfully",
                "data": {},
                "code": 200
            }
    return {
        "message": "there is no post exists with this id",
        "data": {},
        "code": 404
    }