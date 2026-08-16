import asyncio
from app.database import check_connection

print(asyncio.run(check_connection()))