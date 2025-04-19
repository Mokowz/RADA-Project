from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User


@receiver(post_save, User)
def registration_email_confirmation(request):
    current_usr = request.user
    subject = "Welcome to RADA"
    msg = "We are pleased to welcome you here"
    recipient = [current_usr.email]

    send_mail(subject, message=msg, from_emial='ronniemokaya30@gmail.com', recipient_list=recipient)