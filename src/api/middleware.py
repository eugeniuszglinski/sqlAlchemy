import logging
import time

from fastapi import Request

logger = logging.getLogger("src.api.middleware")

async def log_requests(request: Request, call_next: callable):
    start = time.perf_counter()

    logger.info("Started %s %s", request.method, request.url.path)

    response = await call_next(request)

    duration = time.perf_counter() - start
    logger.info(
        "Completed %s %s -> %s in %.4fs",
        request.method,
        request.url.path,
        response.status_code,
        duration,
    )
    return response
