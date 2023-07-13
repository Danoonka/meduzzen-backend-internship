import os
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from run import env_path

load_dotenv(dotenv_path=env_path)


async def connect_to_postgres():
    engine = create_async_engine(os.getenv('POSTGRES_DSN'), echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        async with session.begin():
            create_table_stmt = text("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name VARCHAR(255))")
            await session.execute(create_table_stmt)
    return async_session


async def startup():
    app.state.postgres_session = await connect_to_postgres()


async def shutdown():
    await app.state.postgres_session.close()
    await app.state.postgres_session.wait_closed()


app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)
