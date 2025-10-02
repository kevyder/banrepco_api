import json

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination
from pydantic import ValidationError
from src.routes.v1 import inflation as inflation_router
from src.routes.v1 import trm as trm_router

app = FastAPI()


# override the default validation error handler
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    exc_json = json.loads(exc.json())
    response = {"message": []}
    for error in exc_json:
        response['message'].append(error['loc'][-1]+f": {error['msg']}")

    return JSONResponse(response, status_code=422)


# Add routes
app.include_router(inflation_router.router, prefix="/v1", tags=["inflation"])
app.include_router(trm_router.router, prefix="/v1", tags=["trm"])

# Add pagination support
add_pagination(app)
