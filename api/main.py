from fastapi import FastAPI
from fastapi_pagination import add_pagination
from src.routes.v1 import inflation as inflation_router
from src.routes.v1 import trm as trm_router

app = FastAPI()

# Add routes
app.include_router(inflation_router.router, prefix="/v1", tags=["inflation"])
app.include_router(trm_router.router, prefix="/v1", tags=["trm"])

# Add pagination support
add_pagination(app)
