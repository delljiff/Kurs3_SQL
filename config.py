from dotenv import load_dotenv
import os

load_dotenv()

db_config = {
    "host": os.getenv("HOST"),
    "port": os.getenv("PORT"),
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "client_encoding": "utf8"
}