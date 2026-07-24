import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.logger import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        start_time = time.perf_counter()

        response = await call_next(request)

        duration_ms = (time.perf_counter() - start_time) * 1000

        logger.info(
            f"{request.method} "
            f"{request.url.path} "
            f"status={response.status_code} "
            f"duration={duration_ms:.2f}ms"
        )

        return response