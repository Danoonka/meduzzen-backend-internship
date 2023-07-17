import os

from anyio import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

server_port = os.getenv('SERVER_HOST')
server_host = int(os.getenv('SERVER_PORT'))
postgres_dsn = os.getenv('POSTGRES_DSN')
redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')


