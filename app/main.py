from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import logging

from app.api.endpoints import summarizer
from app.middleware.rate_limiter import add_rate_limiting
from app.core.logging import setup_logging, add_logging_middleware

# Logging sozlash
logger = setup_logging()

# FastAPI ilovasi
app = FastAPI(
    title="Smart Summarizer API",
    description="A REST API that summarizes text using AI models",
    version="1.0.0"
)

# Middleware qo'shish
add_rate_limiting(app)
add_logging_middleware(app)  # Logging middleware qo'shildi

# API routelarini qo'shish
app.include_router(summarizer.router, prefix="/api")

# Statik fayllarni ulash
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templatelarni sozlash
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Frontend sahifasini ko'rsatish"""
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    app_logger.info(f"Starting {config.APP_NAME}")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=config.DEBUG)