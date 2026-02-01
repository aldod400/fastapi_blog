from fastapi import FastAPI, Request

from fastapi.templating import Jinja2Templates


app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", include_in_schema=False)
async def home(request: Request) :
    return templates.TemplateResponse(request, "home.html", {"posts": posts, "title": "Home"})


posts: list[dict] = [
    {
        "id": 1,
        "title": "First Post",
        "content": "This is the content of the first post.",
    },
    {
        "id": 2,
        "title": "Second Post",
        "content": "This is the content of the second post.",
    },
    {
        "id": 3,
        "title": "Third Post",
        "content": "This is the content of the third post.",
    },
]