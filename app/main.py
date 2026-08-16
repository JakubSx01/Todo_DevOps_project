from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from app.database import todos_collection
from bson import ObjectId

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
# Global variables for the todos list and the next id
# todos = []
# next_id = 1

async def render_index(request : Request):
    return templates.TemplateResponse(
        request = request,
        name = "index.html",
        context = {
            "todos": await todos_collection.find().to_list(None),
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
        await todos_collection.insert_one({"title": title})
    return await render_index(request)

@app.post("/delete")
async def delete_todo(request : Request):
    form = await request.form()
    todo_id = form.get("id")
    await todos_collection.delete_one({"_id": ObjectId(todo_id)})

    return await render_index(request)
