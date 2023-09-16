from __future__ import absolute_import, unicode_literals
from datetime import timedelta

import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djolowin.settings')

app = Celery('djolowin')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    'blacklist-expired-tokens': {
        'task': 'core.tasks.blacklist_expired_tokens',
        'schedule': crontab(minute=0, hour=0) # Run every day at midnight
    },
    'check-auction-end': {
        'task': 'auction.tasks.check_auction_end',
        'schedule': timedelta(seconds=15),  # Run every 60 seconds
    },
    'check-auction-ending-soon': {
        'task': 'auction.tasks.check_auction_ending_soon',
        'schedule': timedelta(seconds=60),  # Run every 10 minutes
    },
}

