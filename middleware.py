from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import status

import time
from exceptions import RateLimitError
from handlers import RateExceptionHandler
from config import Config

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.requests = {}
        self.max_requests = Config.RATE_LIMIT_MAX_REQUESTS
        self.time_window = Config.RATE_LIMIT_TIME_WINDOW
        self.endpoints = ["/v1/login", "/v1/validate_otp"]
        
    async def dispatch(self, request, call_next):
        if not Config.RATE_LIMIT_ENABLED:
            response = await call_next(request)
            return response
        
        if request.url.path not in self.endpoints:
            response = await call_next(request)
            return response
        
        request_id = request.client.host + request.url.path
        if request_id not in self.requests:
            self.requests[request_id] = []
        
        self.requests[request_id] = [req for req in self.requests[request_id] if req > time.time() - self.time_window]
        
        if len(self.requests[request_id]) >= self.max_requests:
            return RateExceptionHandler()(request, RateLimitError())
        
        response = await call_next(request)
        
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            self.requests[request_id].append(time.time())
            
        return response
    