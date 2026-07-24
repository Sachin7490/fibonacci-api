import time

from starlette.middleware.base import BaseHTTPMiddleware

from app.logger import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start = time.time()

        logger.info(
            f"Incoming {request.method} {request.url.path}"
        )

        response = await call_next(request)

        elapsed = round((time.time() - start) * 1000, 2)

        logger.info(
            f"Completed {request.method} {request.url.path} "
            f"status={response.status_code} "
            f"duration={elapsed}ms"
        )

        return response