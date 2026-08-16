from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
# Global variables for the todos list and the next id
todos = []
next_id = 1

def render_index(request : Request):
    return templates.TemplateResponse(
        request = request,
        name = "index.html",
        context = {
            "todos": todos,
        }
    )

@app.get("/")
async def readpage(request : Request):
    return render_index(request)

@app.post("/add")
async def add_todo(request : Request):

    global next_id

    form = await request.form()
    title = form.get("title")
    if title:
        todos.append({"id": next_id, "title": title})
        next_id += 1
    return render_index(request)

@app.post("/delete")
async def delete_todo(request : Request):
    form = await request.form()
    todo_id = form.get("id")
    for todo in todos:
        if todo["id"] == todo_id:
            todos.remove(todo)
            break
    return render_index(request)
