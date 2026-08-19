from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from contextlib import asynccontextmanager
from pymongo import AsyncMongoClient
from dotenv import load_dotenv
import os
from pymongo.errors import PyMongoError
from fastapi.responses import JSONResponse

load_dotenv()
BASE_PATH = os.getenv("BASE_PATH", "").rsrtip("/")

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncMongoClient(os.getenv("MONGODB_URI"), serverSelectionTimeoutMS=2000)

    db = client[os.getenv("MONGODB_DB")]

    todos_collection = db["todos"]
    
    app.state.mongodb_client = client
    app.state.todos_collection = todos_collection
    
    yield
    
    await client.close()

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="app/templates")

async def render_index(request : Request):
    return templates.TemplateResponse(
        request = request,
        name = "index.html",
        context = {
            "todos": await request.app.state.todos_collection.find().to_list(None),
            "base_path": BASE_PATH,
        }
    )

@app.get("/")
async def readpage(request : Request):
    return await render_index(request)

@app.post("/add")
async def add_todo(request : Request):

    # global next_id

    form = await request.form()
    title = form.get("title")
    if title:
        await request.app.state.todos_collection.insert_one({"title": title})
    return await render_index(request)

@app.post("/delete")
async def delete_todo(request : Request):
    form = await request.form()
    todo_id = form.get("id")
    await request.app.state.todos_collection.delete_one({"_id": ObjectId(todo_id)})

    return await render_index(request)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/ready")
async def readiness_check(request : Request):
    try:
        await request.app.state.mongodb_client.admin.command("ping")
        return JSONResponse(content={"status": "ok"}, status_code=200)
    except PyMongoError as e:
        return JSONResponse(content={"status": "error"}, status_code=503)