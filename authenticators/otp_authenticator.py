import base64
import time
import struct
import hmac
import hashlib

from config import Config

class OTPAuthenticator:
    def get_otp(self, secret_key: str, time_step=Config.OTP_VALIDITY, otp_length=Config.OTP_LENGTH):
        key = base64.b32decode(secret_key.upper())
        current_time = int(time.time())
        time_counter = current_time // time_step
        time_counter_bytes = struct.pack(">Q", time_counter)
        hmac_hash = hmac.new(key, time_counter_bytes, hashlib.sha1).digest()
        
        offset = hmac_hash[-1] & 0x0F
        truncated_hash = hmac_hash[offset:offset + 4]
        binary_code = struct.unpack(">I", truncated_hash)[0] & 0x7FFFFFFF
        otp = binary_code % (10 ** otp_length)
        
        return str(otp).zfill(otp_length)
    
    def verify_otp(self, secret_key: str, otp: str, time_step=Config.OTP_VALIDITY):
        valid_otp = self.get_otp(secret_key, time_step)
        return valid_otp == otp