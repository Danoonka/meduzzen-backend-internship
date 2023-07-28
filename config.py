import os
from dotenv import load_dotenv

load_dotenv()

server_port = os.getenv('SERVER_HOST')
server_host = int(os.getenv('SERVER_PORT'))
postgres_dsn = os.getenv('POSTGRES_DSN')
redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')
postgres_dsn_alembic = os.getenv('POSTGRES_DSN_ALEMBIC')
DB_USER_TEST = os.getenv('DB_USER_TEST')
DB_PASS_TEST = os.getenv('DB_PASS_TEST')
DB_HOST_TEST = os.getenv('DB_HOST_TEST')
DB_PORT_TEST = os.getenv('DB_PORT_TEST')
DB_NAME_TEST = os.getenv('DB_NAME_TEST')

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

DOMAIN = os.getenv("DOMAIN")
API_AUDIENCE = os.getenv("API_AUDIENCE")
ISSUER = os.getenv("ISSUER")
ALGORITHMS = os.getenv("ALGORITHMS")
