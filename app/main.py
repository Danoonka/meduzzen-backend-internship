from dotenv import load_dotenv
from pathlib import Path
import os
from fastapi import FastAPI

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
print(env_path)
server_port = os.getenv('SERVER_PORT')
print(server_port)

app = FastAPI()


@app.get("/")
async def root():
    return {
        "status_code": 200,
        "detail": "ok",
        "result": "working"
    }
