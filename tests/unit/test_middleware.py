import pytest
from unittest.mock import Mock, AsyncMock, patch
from fastapi.requests import Request
from fastapi import status

from middleware import RateLimitMiddleware
from config import Config


class Endpoints:
    LOGIN = "/v1/login"
    VALIDATE_OTP = "/v1/validate_otp"
    REGISTER = "/v1/register"


class TestRateLimitMiddleware:
    def setup_method(self):
        self.rate_limit_middleware = RateLimitMiddleware(
            app=Mock(), endpoints=[Endpoints.LOGIN, Endpoints.VALIDATE_OTP]
        )

    def _get_request(self, path, ip="127.0.0.1"):
        return Request(
            scope={
                "type": "http",
                "method": "POST",
                "path": path,
                "client": (ip, 1234),
                "headers": [],
            }
        )

    @pytest.mark.asyncio
    async def test_blocks_login_request_when_rate_limit_exceeded_and_ip_is_the_same(
        self,
    ):
        mocked_request = self._get_request(Endpoints.LOGIN)
        call_next_mock = AsyncMock(
            return_value=Mock(status_code=status.HTTP_401_UNAUTHORIZED)
        )

        for _ in range(Config.RATE_LIMIT_MAX_REQUESTS):
            call_next_mock.reset_mock()
            await self.rate_limit_middleware.dispatch(mocked_request, call_next_mock)
            assert call_next_mock.called is True

        call_next_mock.reset_mock()
        await self.rate_limit_middleware.dispatch(mocked_request, call_next_mock)
        assert call_next_mock.called is False

    @pytest.mark.asyncio
    async def test_does_not_block_login_request_when_rate_limit_exceeded_and_ip_is_different(
        self,
    ):
        mocked_request_ip1 = self._get_request(Endpoints.LOGIN, ip="127.0.0.1")
        mocked_request_ip2 = self._get_request(Endpoints.LOGIN, ip="127.0.0.2")

        call_next_mock = AsyncMock(
            return_value=Mock(status_code=status.HTTP_401_UNAUTHORIZED)
        )

        for _ in range(Config.RATE_LIMIT_MAX_REQUESTS):
            call_next_mock.reset_mock()
            await self.rate_limit_middleware.dispatch(
                mocked_request_ip1, call_next_mock
            )
            assert call_next_mock.called is True

        call_next_mock.reset_mock()
        await self.rate_limit_middleware.dispatch(mocked_request_ip2, call_next_mock)
        assert call_next_mock.called is True

    @pytest.mark.asyncio
    async def test_does_not_block_register_request(self):
        mocked_request = self._get_request(Endpoints.REGISTER, ip="127.0.0.1")

        call_next_mock = AsyncMock(
            return_value=Mock(status_code=status.HTTP_401_UNAUTHORIZED)
        )

        for _ in range(Config.RATE_LIMIT_MAX_REQUESTS):
            call_next_mock.reset_mock()
            await self.rate_limit_middleware.dispatch(mocked_request, call_next_mock)
            assert call_next_mock.called is True

        call_next_mock.reset_mock()
        await self.rate_limit_middleware.dispatch(mocked_request, call_next_mock)
        assert call_next_mock.called is True

    @pytest.mark.asyncio
    async def test_unblocks_login_request_when_time_window_is_passed(self):
        with patch("time.time", return_value=0):
            mocked_request = self._get_request(Endpoints.LOGIN)
            call_next_mock = AsyncMock(
                return_value=Mock(status_code=status.HTTP_401_UNAUTHORIZED)
            )

            for _ in range(Config.RATE_LIMIT_MAX_REQUESTS + 1):
                await self.rate_limit_middleware.dispatch(
                    mocked_request, call_next_mock
                )

        with patch("time.time", return_value=Config.RATE_LIMIT_TIME_WINDOW + 1):
            call_next_mock.reset_mock()
            await self.rate_limit_middleware.dispatch(mocked_request, call_next_mock)
            assert call_next_mock.called is True
