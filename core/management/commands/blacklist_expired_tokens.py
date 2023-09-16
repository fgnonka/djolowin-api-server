from django.core.management.base import BaseCommand
from django.utils import timezone
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

class Command(BaseCommand):
    help = 'Blacklist expired refresh tokens'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_tokens = OutstandingToken.objects.filter(token__expires__lt=now)
        for token in expired_tokens:
            token.blacklist()
        self.stdout.write(self.style.SUCCESS('Successfully blacklisted expired tokens.'))