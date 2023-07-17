import os
from dotenv import load_dotenv

load_dotenv()

server_port = os.getenv('SERVER_HOST')
server_host = int(os.getenv('SERVER_PORT'))
postgres_dsn = os.getenv('POSTGRES_DSN')
redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')
postgres_dsn_alembic = os.getenv('POSTGRES_DSN_ALEMBIC')


