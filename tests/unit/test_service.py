import pytest
from unittest.mock import AsyncMock, Mock, create_autospec

from services import AuthenticationService
from entity import UserRegister, UserLogin, OTPValidation
from exceptions import UserAlreadyExistsError, InvalidCredentialsError
from models import User


class TestAuthenticationService:

    def setup_method(self):
        self.user_service = AuthenticationService(
            mail_service=Mock(), jwtAuth=Mock(), otpAuth=Mock(), user_repository=Mock()
        )

    @pytest.mark.asyncio
    async def test_register_ok(self):
        userRegister = UserRegister(
            email="prova@gmail.com", password="password", enable_tfa=False
        )

        self.user_service.user_repository.find_user_by_email = AsyncMock(return_value=None)
        self.user_service.user_repository.add_user = AsyncMock()

        await self.user_service.register(userRegister)
        self.user_service.user_repository.find_user_by_email.assert_called_once_with(
            userRegister.email
        )
        self.user_service.user_repository.add_user.assert_called_once()

    @pytest.mark.asyncio
    async def test_register_throws_error_when_user_already_exists(self):
        userRegister = UserRegister(
            email="prova@gmail.com", password="password", enable_tfa=False
        )

        mock_user = Mock()

        self.user_service.user_repository.find_user_by_email = AsyncMock(
            return_value=mock_user
        )
        self.user_service.user_repository.add_user = AsyncMock()

        with pytest.raises(UserAlreadyExistsError) as e:
            await self.user_service.register(userRegister)

        self.user_service.user_repository.find_user_by_email.assert_called_once_with(
            userRegister.email
        )
        self.user_service.user_repository.add_user.assert_not_called()

    @pytest.mark.asyncio
    async def test_login_no_tfa_ok(self):
        userLogin = UserLogin(email="prova@gmail.com", password="password")

        mock_user = create_autospec(User)
        mock_user.email = "prova@gmail.com"
        mock_user.password = "password"
        mock_user.enable_tfa = False

        self.user_service.user_repository.find_user_by_email = AsyncMock(
            return_value=mock_user
        )
        self.user_service.jwtAuth.generate_access_token = Mock(
            return_value="access_token"
        )

        await self.user_service.login(userLogin)
        self.user_service.jwtAuth.generate_access_token.assert_called_once()

    @pytest.mark.asyncio
    async def test_login_with_tfa_ok(self):
        userLogin = UserLogin(email="prova@gmail.com", password="password")

        mock_user = create_autospec(User)
        mock_user.email = "prova@gmail.com"
        mock_user.password = "password"
        mock_user.enable_tfa = True

        self.user_service.user_repository.find_user_by_email = AsyncMock(
            return_value=mock_user
        )
        self.user_service.jwtAuth.generate_access_token = Mock(
            return_value="access_token"
        )
        self.user_service.otpAuth.get_otp = Mock(return_value="123456")

        await self.user_service.login(userLogin)
        self.user_service.jwtAuth.generate_access_token.assert_not_called()
        self.user_service.otpAuth.get_otp.assert_called_once()

    @pytest.mark.asyncio
    async def test_login_throws_error_when_user_does_not_exists(self):
        userLogin = UserLogin(email="prova@gmail.com", password="password")

        self.user_service.user_repository.find_user_by_email = AsyncMock(return_value=None)
        self.user_service.jwtAuth.generate_access_token = Mock()
        self.user_service.otpAuth.get_otp = Mock()

        with pytest.raises(InvalidCredentialsError) as e:
            await self.user_service.login(userLogin)

        self.user_service.jwtAuth.generate_access_token.assert_not_called()
        self.user_service.otpAuth.get_otp.assert_not_called()

    @pytest.mark.asyncio
    async def test_authenticate_otp_ok(self):
        otpValidation = OTPValidation(email="prova@gmail.com", otp="123456")

        mock_user = create_autospec(User)
        mock_user.email = "prova@gmail.com"
        mock_user.password = "password"
        mock_user.enable_tfa = True

        self.user_service.user_repository.find_user_by_email = AsyncMock(
            return_value=mock_user
        )
        self.user_service.otpAuth.verify_otp = Mock(return_value=True)
        self.user_service.jwtAuth.generate_access_token = Mock(return_value="access_token")

        await self.user_service.validate_otp(otpValidation)
        self.user_service.jwtAuth.generate_access_token.assert_called_once()

    @pytest.mark.asyncio
    async def test_authenticate_otp_throws_error_when_user_does_not_exist(self):
        otpValidation = OTPValidation(email="prova@gmail.com", otp="123456")

        self.user_service.user_repository.find_user_by_email = AsyncMock(return_value=None)
        self.user_service.jwtAuth.generate_access_token = Mock()

        with pytest.raises(InvalidCredentialsError) as e:
            await self.user_service.validate_otp(otpValidation)

        self.user_service.jwtAuth.generate_access_token.assert_not_called()
