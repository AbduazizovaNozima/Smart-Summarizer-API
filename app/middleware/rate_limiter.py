import time
from fastapi import FastAPI, Request, HTTPException
from typing import Dict, Tuple
import logging

logger = logging.getLogger("summarizer.middleware")


class RateLimiter:
    def __init__(self, requests_limit=10, window_seconds=60):
        self.requests_limit = requests_limit
        self.window_seconds = window_seconds
        self.clients: Dict[str, Tuple[int, float]] = {}

    def is_rate_limited(self, client_id: str) -> bool:
        current_time = time.time()

        if client_id not in self.clients or current_time - self.clients[client_id][1] > self.window_seconds:
            self.clients[client_id] = (1, current_time)
            return False

        requests_count, window_start = self.clients[client_id]

        if requests_count < self.requests_limit:
            self.clients[client_id] = (requests_count + 1, window_start)
            return False

        return True


rate_limiter = RateLimiter()


def add_rate_limiting(app: FastAPI):

    @app.middleware("http")
    async def rate_limit_middleware(request: Request, call_next):
        if request.url.path.startswith("/api/"):
            client_id = request.client.host if request.client and request.client.host else "test-client"

            if rate_limiter.is_rate_limited(client_id):
                logger.warning(f"Rate limit exceeded: {client_id}")
                raise HTTPException(
                    status_code=429,
                    detail="Too many requests. Please try again later."
                )


        return await call_next(request)