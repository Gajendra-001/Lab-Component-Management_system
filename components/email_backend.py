from django.core.mail.backends.smtp import EmailBackend
import ssl

class CustomEmailBackend(EmailBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection_params = {
            'timeout': 30,
            'source_address': None
        }

    def open(self):
        if self.connection:
            return False
        
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            self.connection = self.connection_class(
                self.host, self.port, **self.connection_params
            )
            if self.use_tls:
                self.connection.starttls(context=context)
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except Exception:
            if not self.fail_silently:
                raise 