from django.utils import timezone

from celery import shared_task
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken


@shared_task
def blacklist_expired_tokens():
    now = timezone.now()
    expired_tokens = OutstandingToken.objects.filter(expires_at__lt=now)
    for token in expired_tokens:
        BlacklistedToken.objects.get_or_create(token=token)
    return 'Successfully blacklisted expired tokens.'