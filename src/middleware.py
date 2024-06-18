from abc import ABC, abstractmethod
from typing import List, Dict
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import status
from fastapi.requests import Request
import time

from exceptions import RateLimitError
from handlers import RateExceptionHandler
from config import Config


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, endpoints=[]):
        super().__init__(app)
        self.endpoints = endpoints
        self.storage: RateLimitStorage = InMemoryRateLimitStorage()

    async def dispatch(self, request, call_next):
        if not Config.RATE_LIMIT_ENABLED:
            response = await call_next(request)
            return response

        if request.url.path not in self.endpoints:
            response = await call_next(request)
            return response

        request_id = self._get_request_id(request)

        self.storage.clear_requests(request_id, Config.RATE_LIMIT_TIME_WINDOW)
        requests = self.storage.get_requests(request_id)

        if len(requests) >= Config.RATE_LIMIT_MAX_REQUESTS:
            return RateExceptionHandler()(request, RateLimitError())

        response = await call_next(request)

        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            self.storage.store_request(request_id, time.time())

        return response

    def _get_request_id(self, request: Request) -> str:
        return request.client.host + request.url.path
    
    
class RateLimitStorage(ABC):
    @abstractmethod
    def store_request(self, request_id: str, timestamp: float) -> None:
        pass

    @abstractmethod
    def get_requests(self, request_id: str, time_window: int) -> List[float]:
        pass

    @abstractmethod
    def clear_requests(self, request_id: str) -> None:
        pass


class InMemoryRateLimitStorage(RateLimitStorage):
    def __init__(self):
        self.requests: Dict[str, List[float]] = {}

    def store_request(self, request_id: str, timestamp: float) -> None:
        if request_id not in self.requests:
            self.requests[request_id] = []
        self.requests[request_id].append(timestamp)

    def get_requests(self, request_id: str):
        return self.requests.get(request_id, [])

    def clear_requests(self, request_id: str, time_window: int) -> None:
        if request_id not in self.requests:
            self.requests[request_id] = []

        self.requests[request_id] = [ req for req in self.requests[request_id] if req > time.time() - time_window ]
