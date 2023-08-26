from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

def send_verification_email(user, verification_link):
    subject = 'Verify Your Email'
    message = f'Hi {user.username}, please click the link below to verify your email:\n\n{verification_link}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)


def send_reset_password_email(user, reset_link):
    
    # Send the email to the user
    subject="Password Reset",
    message=f"Hi {user.username}, Click the link below to reset your password:\n\n{reset_link}"
    from_email = settings.DEFAULT_FROM_EMAIL,
    recipient_list = [user.email],
    
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)