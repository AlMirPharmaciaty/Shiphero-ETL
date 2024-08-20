import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv('DB_URL')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
