import logging
import os
from datetime import datetime
import aiofiles
from fastapi import Request, Response
from typing import Callable


def setup_logging():
    """Asosiy logging sozlash"""
    # Logs papkasini yaratish
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(level=logging.WARNING)  # Boshqa kutubxonalar uchun WARNING darajasi


    # Asosiy logger
    logger = logging.getLogger("summarizer")
    logger.setLevel(logging.INFO)

    # Agar handler mavjud bo'lmasa
    if not logger.handlers:
        # Fayl handleri
        file_handler = logging.FileHandler("logs/app.log")
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        ))
        logger.addHandler(file_handler)

        # Konsol handleri
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        ))
        logger.addHandler(console_handler)

        # Transformers kutubxonasi loglarini o'chirish
        # logging.getLogger("transformers").setLevel(logging.ERROR)
        # logging.getLogger("filelock").setLevel(logging.ERROR)
        # logging.getLogger("huggingface_hub").setLevel(logging.ERROR)

    return logger


async def log_request(request: Request, status_code: int, processing_time: float = None):
    """So'rov tafsilotlarini access.log fayliga yozish"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Status kodga asoslangan log darajasi
    if 200 <= status_code < 300:
        level = "INFO"
    elif 400 <= status_code < 500:
        level = "WARNING"
    else:
        level = "ERROR"

    # Log xabarini formatlash
    log_msg = (
        f"time: {timestamp} -- "
        f"level: {level} -- "
        f"status: {status_code} -- "
        f"method: {request.method} -- "
        f"path: {request.url.path} -- "
        f"client: {request.client.host}"
    )

    # Qayta ishlash vaqtini qo'shish agar mavjud bo'lsa
    if processing_time is not None:
        log_msg += f" -- processing_time: {processing_time:.4f}s"

    # Access log fayliga yozish
    async with aiofiles.open("logs/access.log", "a") as f:
        await f.write(log_msg + "\n")


def add_logging_middleware(app):
    """Logging middleware qo'shish"""

    @app.middleware("http")
    async def logging_middleware(request: Request, call_next):
        # So'rov boshlanish vaqti
        start_time = datetime.now()

        try:
            # So'rovni qayta ishlash
            response = await call_next(request)

            # Qayta ishlash vaqtini hisoblash
            processing_time = (datetime.now() - start_time).total_seconds()

            # So'rovni log qilish
            await log_request(request, response.status_code, processing_time)

            return response
        except Exception as e:
            # Xatoni log qilish
            logger = logging.getLogger("summarizer")
            logger.error(f"Unhandled exception: {str(e)}")

            # Muvaffaqiyatsiz so'rovni log qilish
            await log_request(request, 500)

            # 500 javob qaytarish
            return Response("Internal Server Error", status_code=500)