from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings

# from .models import User
User = get_user_model()


@receiver(post_save, sender=User)
def registration_email_confirmation(sender, instance, created, **kwargs):
    if created:        
        subject = "Welcome to RADA Early Alert System"
        msg = """
Hi,

Thank you for registering with the Baringo Early Alert System.

You’re now part of a community working together to stay prepared and protected from the effects of floods and droughts in our region.

Here’s what you can expect:
- Weekly predictions for flood and drought risks
- Real-time alerts sent directly to your phone or email
- Visual summaries to help you plan and act early

We’re committed to making sure everyone in Baringo has access to timely, reliable weather information that can help protect lives, livestock, and livelihoods.

If you have any questions or suggestions, feel free to reply to this email. We’d love to hear from you.

Welcome aboard!

Warm regards,  
The Early Alert Team
        """
        recipient = [instance.email]
        sendr = settings.EMAIL_HOST_USER

        send_mail(subject, message=msg, from_email=sendr, recipient_list=recipient)
