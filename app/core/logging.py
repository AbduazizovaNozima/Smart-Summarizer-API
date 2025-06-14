import logging
import os
from datetime import datetime
import aiofiles
from fastapi import Request, Response


def setup_logging():
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(level=logging.WARNING)

    logger = logging.getLogger("summarizer")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler("logs/app.log")
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        ))
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        ))
        logger.addHandler(console_handler)

    return logger


async def log_request(request: Request, status_code: int, processing_time: float = None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if 200 <= status_code < 300:
        level = "INFO"
    elif 400 <= status_code < 500:
        level = "WARNING"
    else:
        level = "ERROR"

    client_host = request.client.host if request.client and request.client.host else "unknown"

    log_msg = (
        f"time: {timestamp} -- "
        f"level: {level} -- "
        f"status: {status_code} -- "
        f"method: {request.method} -- "
        f"path: {request.url.path} -- "
        f"client: {client_host}"
    )

    if processing_time is not None:
        log_msg += f" -- processing_time: {processing_time:.4f}s"

    async with aiofiles.open("logs/access.log", "a") as f:
        await f.write(log_msg + "\n")



def add_logging_middleware(app):

    @app.middleware("http")
    async def logging_middleware(request: Request, call_next):
        start_time = datetime.now()

        try:
            response = await call_next(request)
            processing_time = (datetime.now() - start_time).total_seconds()
            await log_request(request, response.status_code, processing_time)
            return response

        except Exception as e:
            logger = logging.getLogger("summarizer")
            logger.error(f"Unhandled exception: {str(e)}")

            await log_request(request, 500)

            return Response("Internal Server Error", status_code=500)