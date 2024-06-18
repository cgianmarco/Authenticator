class MailService:
    def send_otp_mail(self, email, otp):
        print(f"OTP {otp} sent to {email}")