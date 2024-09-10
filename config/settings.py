import os
from dotenv import load_dotenv

load_dotenv()

ENV = 'DEV'
#ENV = 'PROD'

DB_URL_DEV = os.getenv('DB_URL_DEV')
DB_URL_PROD = os.getenv('DB_URL_PROD')

AUTH_TOKEN_STAG = os.getenv('AUTH_TOKEN_STAG')
AUTH_TOKEN_PROD = os.getenv('AUTH_TOKEN_PROD')

if ENV == "PROD":
    DB_URL = DB_URL_PROD
    AUTH_TOKEN = AUTH_TOKEN_PROD
else:
    DB_URL = DB_URL_DEV
    AUTH_TOKEN = AUTH_TOKEN_STAG
