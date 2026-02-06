from datetime import datetime
from fastapi import FastAPI, Request, HTTPException, status, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from schemas import PostCreate, PostResponse

app = FastAPI()

# Create API router with /api prefix
api_router = APIRouter(prefix="/api")

templates = Jinja2Templates(directory="templates")

static_files_path = "static"

app.mount("/static", StaticFiles(directory=static_files_path), name="static")

@app.get("/", include_in_schema=False, name="home")
async def home(request: Request) :
    return templates.TemplateResponse(request, "home.html", {"posts": posts, "title": "Home"})

@app.get("/posts/{id}", include_in_schema=False, name="post_detail")
def post_detail(request: Request, id: int) -> dict:
    for post in posts:
        if post.get("id") == id:
            return templates.TemplateResponse(request, "post.html", {"post": post, "title": post["title"][:50]})

    return templates.TemplateResponse(
        request, "error.html",
          {"title": "Post Not Found", 
           "status_code": status.HTTP_404_NOT_FOUND,
             "message": "The post you are looking for does not exist."
             },
            status_code=status.HTTP_404_NOT_FOUND
            )


posts: list[dict] = [
    {
        "id"         : 1,
        "title"      : "First Post",
        "content"    : "This is the content of the first post.",
        "author"     : "Elghonemy",
        "date_posted": "April 20, 2024",
    },
    {
        "id"         : 2,
        "title"      : "Second Post",
        "content"    : "This is the content of the second post.",
        "author"     : "Elghonemy",
        "date_posted": "April 21, 2024",
    },
    {
        "id"     : 3,
        "title"  : "Third Post",
        "content": "This is the content of the third post.",
        "author" : "Elghonemy",
        "date_posted": "April 22, 2024"
    },
]

@api_router.get("/posts", response_model=list[PostResponse])
async def get_posts()-> list[dict]:
    return posts

@api_router.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate) -> PostResponse:
    new_post = {
        "id": len(posts) + 1,
        "title": post.title,
        "content": post.content,
        "author": post.author,
        "date_posted": datetime.now().strftime("%B %d, %Y")
    }
    posts.append(new_post)
    return new_post

@api_router.get("/posts/{id}", response_model=PostResponse)
def post_detail_api(id: int) -> PostResponse:
    for post in posts:
        if post.get("id") == id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

# Include API router
app.include_router(api_router)


@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = exception.detail or "An error occurred."

    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=exception.status_code,
            content={
                "message": message
                }
        )
    
    return templates.TemplateResponse(
        request, "error.html",
        {"title": f"{exception.status_code} Error", "status_code": exception.status_code, "message": message},
        status_code=exception.status_code
    )

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):

    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )
    
    return templates.TemplateResponse(
        request, "error.html",
        {"title": "Validation Error", "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT, "message": "There was a validation error with your request."},
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
    )