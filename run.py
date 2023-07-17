import uvicorn
from app.main import app
from config import server_port, server_host

if __name__ == "__main__":
    uvicorn.run(app, host=server_port, port=server_host, reload=True)
