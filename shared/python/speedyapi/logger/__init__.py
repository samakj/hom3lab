import logging
from typing import Any

LOG = logging.getLogger("uvicorn")


class Logger:
    def debug(self, *args: Any, **kwargs: Any) -> None:
        LOG.debug(*args, **kwargs)

    def info(self, *args: Any, **kwargs: Any) -> None:
        LOG.info(*args, **kwargs)

    def warning(self, *args: Any, **kwargs: Any) -> None:
        LOG.warning(*args, **kwargs)

    def error(self, *args: Any, **kwargs: Any) -> None:
        LOG.error(*args, **kwargs)

    def exception(self, *args: Any, **kwargs: Any) -> None:
        LOG.exception(*args, **kwargs)
