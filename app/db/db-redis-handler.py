import os
from dotenv import load_dotenv
from sqlalchemy.testing import asyncio
from app.main import app
from run import env_path

load_dotenv(dotenv_path=env_path)


async def connect_to_redis():
    redis = await asyncio.create_redis_pool(f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}")
    return redis


async def startup():
    app.state.redis = await connect_to_redis()


async def shutdown():
    app.state.redis.close()
    await app.state.redis.wait_closed()


app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)
