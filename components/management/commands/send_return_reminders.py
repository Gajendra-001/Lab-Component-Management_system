from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from components.models import ComponentCheckout

class Command(BaseCommand):
    help = 'Sends email reminders to users about upcoming component returns'

    def handle(self, *args, **options):
        # Get checkouts that are due in 2 days and haven't been returned
        due_date = timezone.now().date() + timedelta(days=2)
        checkouts = ComponentCheckout.objects.filter(
            expected_return_date=due_date,
            actual_return_date__isnull=True
        ).select_related('component', 'checked_out_by')

        for checkout in checkouts:
            # Get display name from checkout
            display_name = checkout.display_name or checkout.checked_out_by.get_full_name() or checkout.checked_out_by.username
            
            # Prepare email content
            subject = f'Reminder: Component Return Due in 2 Days'
            context = {
                'component': checkout.component,
                'checkout': checkout,
                'due_date': checkout.expected_return_date,
            }
            
            # Render email templates
            message = render_to_string('components/email/return_reminder.txt', context)
            html_message = render_to_string('components/email/return_reminder.html', context)

            # Send email
            send_mail(
                subject=subject,
                message=message,
                from_email=(display_name, 'dhaked1415@gmail.com'),  # Use display name in from field
                recipient_list=[checkout.user_email],
                html_message=html_message,
                fail_silently=False,
            )

            self.stdout.write(
                self.style.SUCCESS(f'Successfully sent reminder to {checkout.user_email}')
            ) 