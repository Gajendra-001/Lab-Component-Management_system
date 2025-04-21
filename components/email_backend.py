from django.core.mail.backends.smtp import EmailBackend
import ssl
from email.utils import formataddr

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

    def _send(self, email_message):
        """A helper method that does the actual sending."""
        if not email_message.recipients():
            return False
        try:
            # Format the from_email with display name if provided
            if isinstance(email_message.from_email, tuple):
                from_email = formataddr(email_message.from_email)
            else:
                from_email = email_message.from_email
                
            self.connection.sendmail(
                from_email,
                email_message.recipients(),
                email_message.message().as_bytes(linesep='\r\n'),
            )
            return True
        except Exception:
            if not self.fail_silently:
                raise
            return False 