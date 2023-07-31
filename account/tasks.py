from celery import shared_task
from django.utils import timezone


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken


from .broadcast import send_activation_email, send_welcome_notification, send_welcome_email
from .signals import user_verified


User = get_user_model()

@receiver(post_save, sender=User)
def generate_activation_email(sender, instance, created, **kwargs):
    if created:
        send_activation_email(instance)
        

@receiver(user_verified)
def generate_welcome_notification_and_email(sender, instance, **kwargs):
    send_welcome_notification(instance)
    send_welcome_email(instance)


@shared_task
def blacklist_expired_tokens():
    # Get the current time
    now = timezone.now()
    
    # Get all tokens that have already expired
    expired_tokens = OutstandingToken.objects.filter(expires_at__lte=now)
    
    # Perform actions for expired tokens (e.g., blacklist them)
    for token in expired_tokens:
        # Your actions here to blacklist the token...
        BlacklistedToken.objects.create(token=token)
        token.delete()  # Example: Delete the token record from the database
        print(f"Blacklisted token {token.jti}")