import os

from dotenv import load_dotenv

load_dotenv()

COUNTRIES = ["United States", "Italy", "Germany", "Ireland", "Brazil"]

db_config = {
    "host": os.getenv("HOST"),
    "port": os.getenv("PORT"),
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "client_encoding": "utf8",
}
