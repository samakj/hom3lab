from app_config import config

from shared.python.cache import Cache

cache = Cache(
    host=config["cache"]["host"],
    port=config["cache"]["port"],
    alias=config["cache"].get("alias"),
)
