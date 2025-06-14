from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from app.api import summarizer
from app.middleware.rate_limiter import add_rate_limiting
from app.core.logging import setup_logging, add_logging_middleware
from app.core import config

logger = setup_logging()

app = FastAPI(
    title="Smart Summarizer API",
    description="A REST API that summarizes text using AI models",
    version="1.0.0"
)

add_rate_limiting(app)
add_logging_middleware(app)

app.include_router(summarizer.router, prefix="/api")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


if __name__ == "__main__":
    app_logger.info(f"Starting {config.APP_NAME}")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=config.DEBUG)