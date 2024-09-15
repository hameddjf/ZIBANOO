import time
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import datetime, timedelta

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):

        print(f"Timestamp: {timestamp}")
        return str(user.pk) + str(timestamp) + str(user.is_active)

    def is_token_expired(self, user, timestamp, expiration_minutes=2):
        """
        بررسی می‌کند آیا توکن منقضی شده است یا نه.
        :param user: کاربر
        :param timestamp: زمان ثبت‌شده توکن
        :param expiration_minutes: تعداد دقیقه‌های اعتبار توکن
        :return: True اگر منقضی شده باشد، در غیر این صورت False
        """
        # تبدیل timestamp به datetime
        expiration_time = datetime.fromtimestamp(timestamp) + timedelta(minutes=expiration_minutes)
        print(f"Expiration time: {expiration_time}, Current time: {datetime.now()}")

        # بررسی اینکه آیا توکن منقضی شده یا خیر
        return expiration_time < datetime.now()

account_activation_token = AccountActivationTokenGenerator()
