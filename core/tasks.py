from django.utils import timezone

from celery import shared_task
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken


@shared_task
def blacklist_expired_tokens():
    now = timezone.now()
    expired_tokens = OutstandingToken.objects.filter(token__expires__lt=now)
    for token in expired_tokens:
        token.blacklist()
    return 'Successfully blacklisted expired tokens.'