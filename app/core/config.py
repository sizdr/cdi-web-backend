from dotenv import load_dotenv
import os

load_dotenv()

class DATABASE_CREDENTIALS():
    def __init__(self) -> None:
        self.set_enviroment_variable()

    def set_enviroment_variable(self):
        self.DB_USER = os.getenv('MYSQL_ADDON_USER')
        self.DB_PASSWORD = os.getenv('MYSQL_ADDON_PASSWORD')
        self.DB_HOST = os.getenv('MYSQL_ADDON_HOST')
        self.DB_NAME = os.getenv('MYSQL_ADDON_DB')
        self.DB_PORT = os.getenv('MYSQL_ADDON_PORT')

CREDENTIALS = DATABASE_CREDENTIALS()

CONECTION_URL = f"mysql://{CREDENTIALS.DB_USER}:{CREDENTIALS.DB_PASSWORD}@{CREDENTIALS.DB_HOST}:{CREDENTIALS.DB_PORT}/{CREDENTIALS.DB_NAME}"


SECRET_KEY = os.getenv('SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))