"""Request logging middleware."""

import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """Log HTTP requests."""

    async def dispatch(self, request: Request, call_next):
        """Log request and response."""
        start_time = time.time()
        
        logger.info(f"Request: {request.method} {request.url.path}")
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        logger.info(
            f"Response: {response.status_code} - {process_time:.3f}s"
        )
        
        return response

