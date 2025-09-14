from fastapi import FastAPI
from fastapi_pagination import add_pagination
from src.routes.v1 import inflation as inflation_router

app = FastAPI()

# Add routes
app.include_router(inflation_router.router, prefix="/v1", tags=["inflation"])

# Add pagination support
add_pagination(app)
