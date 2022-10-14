import base64
from datetime import datetime

import pyotp

from pewbill.settings import OTP_EXPIRY_TIME


class PewBillOTP:

    def __init__(self):
        self.name = "PewBillOTP"

    def generate_key(self, data):
        return str(data) + str(datetime.date(datetime.now())) + "Some Random Secret Key"

    def create_otp(self, data):
        key = base64.b32encode(self.generate_key(data).encode())  # Key is generated
        otp = pyotp.TOTP(key, interval=OTP_EXPIRY_TIME, issuer="PewBill")
        user_otp = otp.now()
        return user_otp

    def verify_otp_phone(self, data):
        key = base64.b32encode(self.generate_key(data['phoneNumber']).encode())  # Generating Key
        otp_new = pyotp.TOTP(key, interval=OTP_EXPIRY_TIME, issuer="PewBill")  # TOTP Model
        if otp_new.verify(data.get('otp')):
            return True
        return False

    def verify_otp_email(self, data):
        key = base64.b32encode(self.generate_key(data['email']).encode())  # Generating Key
        otp_new = pyotp.TOTP(key, interval=OTP_EXPIRY_TIME, issuer="PewBill")  # TOTP Model
        if otp_new.verify(data.get('otp')):
            return True
        return False
