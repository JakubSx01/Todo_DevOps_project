from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
import pytest
import os
from dotenv import load_dotenv

load_dotenv(".env.test", override=True)

# Testujemy również generowanie linków dla Tailscale Funnel
os.environ["BASE_PATH"] = "/todo-devops-project"

from app.main import app

pytestmark = pytest.mark.asyncio(loop_scope="module")


async def test_index():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)

        async with AsyncClient(
            transport=transport,
            base_url="http://testserver"
        ) as client:

            response = await client.get("/")

            assert response.status_code == 200
            assert "Todo App" in response.text
            assert 'action="/todo-devops-project/add"' in response.text


async def test_add_todo():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)

        async with AsyncClient(
            transport=transport,
            base_url="http://testserver"
        ) as client:

            response = await client.post(
                "/add",
                data={"title": "Test Todo"}
            )

            assert response.status_code == 200
            assert "Test Todo" in response.text


async def test_delete_todo():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)

        async with AsyncClient(
            transport=transport,
            base_url="http://testserver"
        ) as client:

            result = await app.state.todos_collection.insert_one({
                "title": "Test Todo Delete"
            })

            data = {
                "id": str(result.inserted_id)
            }

            response = await client.post(
                "/delete",
                data=data
            )

            assert response.status_code == 200

            deleted = await app.state.todos_collection.find_one({
                "_id": result.inserted_id
            })

            assert deleted is None
            assert 'action="/todo-devops-project/delete"' in response.text