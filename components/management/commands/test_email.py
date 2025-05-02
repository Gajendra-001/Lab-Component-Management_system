from django.core.management.base import BaseCommand
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'Test email configuration by sending a test email'

    def handle(self, *args, **options):
        try:
            send_mail(
                subject='Test Email from IoT Lab',
                message='This is a test email to verify your email configuration is working correctly.',
                from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings
                recipient_list=['dhaked1415@gmail.com'],  # Send to yourself
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS('Test email sent successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to send test email: {str(e)}')) 