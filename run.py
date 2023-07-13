import os
import uvicorn
from pathlib import Path
from dotenv import load_dotenv

from app.main import app

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv('SERVER_HOST'), port=int(os.getenv('SERVER_PORT')), reload=True)
