from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from app.api import summarizer
from app.middleware.rate_limiter import rate_limiter
from app.core.logging import setup_logging
from app.core import config

logger = setup_logging()

app = FastAPI(
    title="Smart Summarizer API",
    description="A REST API that summarizes text using AI models",
    version="1.0.0"
)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    if request.url.path.startswith("/api/"):
        client_ip = request.client.host if request.client and request.client.host else "unknown"
        allowed = await rate_limiter(client_ip)

        if not allowed:
            logger.warning(f"Rate limit exceeded: {client_ip}")
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later."
            )

    response = await call_next(request)
    return response

app.include_router(summarizer.router, prefix="/api")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    logger.info(f"Starting {config.APP_NAME}")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=config.DEBUG)
