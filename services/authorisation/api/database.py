from app_config import config

from shared.python.database import Database

database = Database(
    host=config["db"]["host"],
    port=config["db"]["port"],
    user=config["db"]["user"],
    password=config["db"]["password"],
    name=config["db"].get("name"),
)
