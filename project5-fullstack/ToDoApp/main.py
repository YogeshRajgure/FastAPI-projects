
from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import Field

from .database import engine, SessionLocal
from .models import Base

from .routers import auth, todos, admin, user


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="ToDoApp/static"), name="static")


@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)

@app.get("/healthy")
def health_check():
    return {'status': 'healthy'}

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(user.router)
app.include_router(todos.router)

