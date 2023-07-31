from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

def send_verification_email(user):
    verification_link = reverse('authentication:verify-email', args=[str(user.verification_token)])

    subject = 'Verify Your Email'
    message = f'Hi {user.username}, please click the link below to verify your email:\n\n{settings.BASE_URL}{verification_link}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)


def send_reset_password_email(user):
    # Define the reset password link URL (replace example.com with your domain)
    reset_link = reverse('authentication:password-reset', args=[str(user.reset_password_token)])

    # Send the email to the user
    subject="Password Reset",
    message=f"Hi {user.username}, Click the link below to reset your password:\n\n{settings.BASE_URL}{reset_link}"
    from_email = settings.DEFAULT_FROM_EMAIL,
    recipient_list = [user.email],
    
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)