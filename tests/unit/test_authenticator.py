import pytest
from unittest.mock import Mock, patch

from authenticators import JWTAuthenticator, OTPAuthenticator
from config import Config

class TestJwtAuthenticator:
    def setup_method(self):
        self.jwt_authenticator = JWTAuthenticator()
        
    def test_generate_access_token_ok(self):
        user = Mock()
        user.id = 1
        user.email = "prova@gmail.com"
        
        access_token = self.jwt_authenticator.generate_access_token(user)
        
        assert access_token is not None
        
    def test_generate_access_token_throws_error_when_user_is_none(self):
        with pytest.raises(Exception) as e:
            self.jwt_authenticator.generate_access_token(None)
            

class TestOTPAuthenticator:
    def setup_method(self):
        self.otp_authenticator = OTPAuthenticator()
        self.secret_key = "XzoQxR7Czn3JudigQvjqopir3mBE2uRI"
        
    def test_get_otp_ok(self):
        otp = self.otp_authenticator.get_otp(self.secret_key)
        assert otp is not None
        
    def test_get_otp_throws_error_when_secret_key_is_none(self):
        with pytest.raises(Exception) as e:
            self.otp_authenticator.get_otp(None)
            
    def test_verify_otp_ok(self):
        otp = self.otp_authenticator.get_otp(self.secret_key)
        verified = self.otp_authenticator.verify_otp(self.secret_key, otp)
        
        assert verified is True
        
    def test_verify_otp_is_false_when_otp_is_wrong(self):
        otp = self.otp_authenticator.get_otp(self.secret_key)
        verified = self.otp_authenticator.verify_otp(self.secret_key, "123")
        
        assert verified is False
        
    def test_verify_otp_is_false_when_secret_key_is_wrong(self):
        otp = self.otp_authenticator.get_otp(self.secret_key)
        verified = self.otp_authenticator.verify_otp("KBJE6VSB", otp)
        
        assert verified is False
        
    def test_verify_otp_expires_when_one_minute_has_passed(self):
        with patch('time.time', return_value=0):
            otp = self.otp_authenticator.get_otp(self.secret_key)
            
        with patch('time.time', return_value=Config.OTP_VALIDITY + 1):
            verified = self.otp_authenticator.verify_otp(self.secret_key, otp)
        
        assert verified is False
        
    def test_verify_otp_is_valid_when_thirty_seconds_have_passed(self):
        with patch('time.time', return_value=0):
            otp = self.otp_authenticator.get_otp(self.secret_key)
            
        with patch('time.time', return_value=Config.OTP_VALIDITY // 2):
            verified = self.otp_authenticator.verify_otp(self.secret_key, otp)
        
        assert verified is True