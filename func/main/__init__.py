import imp
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import azure.functions as afunc

from ..utilities.exceptions import ApiException
from ..routers import checkouts
from opencensus.ext.azure.log_exporter import AzureLogHandler
import os


description = """
This is a Sale and Stock API. 

## Checkouts
* Add checkouts
* Retrieve checkouts
* Retrieve a specific checkout by ID
* Update existing checkouts
* Delete checkouts by ID
"""

app = FastAPI(
    title="Sale and Stock API.",
    description=description,
    version="0.1",
    contact={
        "name": "Shinichi Takano",
        # "url": "https://",
        "email": "s-takano@cd6.so-net.ne.jp"
    },
    license_info= {
        "name": "MIT License",
        "url": "https://github.com/s-takano/ptail_ubiapi.git/LICENSE"
    }
)

# Add api routers here
app.include_router(checkouts.router)


@app.exception_handler(ApiException)
async def generic_api_exception_handler(request: Request, ex:  ApiException):
    return JSONResponse(
        status_code=ex.status_code,
        content={
            "code": ex.code,
            "description": ex.description
        }
    )


def main(req: afunc.HttpRequest, context: afunc.Context) -> afunc.HttpResponse:
    get_logger().info(f'HTTP trigger function {req.url}')
    return afunc.AsgiMiddleware(app).handle(req, context)

def get_logger():
    instrument_key = os.environ["APPINSIGHTS_INSTRUMENTATIONKEY"]
    logger = logging.getLogger(__name__)
    logger.setLevel(10)
    logger.addHandler(AzureLogHandler(connection_string=f'InstrumentationKey={instrument_key}'))
    return logger
