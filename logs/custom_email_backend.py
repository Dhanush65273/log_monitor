import ssl
from django.core.mail.backends.smtp import EmailBackend


class CustomEmailBackend(EmailBackend):

    def open(self):
        if self.connection:
            return False

        self.ssl_context = ssl._create_unverified_context()

        return super().open()
