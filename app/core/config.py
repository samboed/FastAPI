import os

from dotenv import load_dotenv


load_dotenv()

DEBUG = True
#DEBUG = bool(os.getenv('DEBUG', False) == 'True')

DB_DRIVER = os.getenv('DB_DRIVER', 'postgresql+asyncpg')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = int(os.getenv('DB_PORT', 5432))
DB_NAME = os.getenv('DB_NAME', 'advertisement_db')

DB_DSN = f'{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'