from routes.devices import DEVICES_V0_ROUTER
from routes.locations import LOCATIONS_V0_ROUTER
from routes.measurements import MEASUREMENTS_V0_ROUTER
from routes.metrics import METRICS_V0_ROUTER

from shared.python.speedyapi import SpeedyAPI

app = SpeedyAPI()

# app.db = database
# app.cache = cache

app.include_router(DEVICES_V0_ROUTER)
app.include_router(LOCATIONS_V0_ROUTER)
app.include_router(MEASUREMENTS_V0_ROUTER)
app.include_router(METRICS_V0_ROUTER)


@app.on_event("startup")  # type: ignore
async def startup() -> None:
    # app.db.logger = app.logger
    # app.cache.logger = app.logger
    # await app.db.initialise()
    # await app.cache.initialise()
    pass