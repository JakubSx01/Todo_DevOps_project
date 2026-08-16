from fastapi.testclient import TestClient
import pytest
from dotenv import load_dotenv
load_dotenv(".env.test", override=True)

from app.main import app
from app.database import todos_collection
client = TestClient(app)
pytestmark = pytest.mark.asyncio(loop_scope="module")

def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert "Todo App" in response.text

def test_add_todo():
    response = client.post("/add", data={"title": "Test Todo"})
    assert response.status_code == 200
    assert "Test Todo" in response.text

@pytest.mark.asyncio
async def test_delete_todo():
    result = await todos_collection.insert_one({"title": "Test Todo Delete"})
    data = {"id": str(result.inserted_id)}
    response = client.post("/delete", data=data)
    deleted = await todos_collection.find_one({"_id": result.inserted_id})
    assert deleted is None