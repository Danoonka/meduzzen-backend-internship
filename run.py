import os
import uvicorn
from dotenv import load_dotenv

from app.main import app

load_dotenv()

if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv('SERVER_HOST'), port=int(os.getenv('SERVER_PORT')), reload=True)
