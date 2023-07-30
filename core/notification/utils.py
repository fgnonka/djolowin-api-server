from django.contrib.sites.models import Site
from django.contrib.staticfiles.storage import staticfiles_storage

from core.utils import build_absolute_uri

LOGO_URL = build_absolute_uri(staticfiles_storage.url("images/djolowin_logo.png"))


def get_site_context():
    """Returns site context"""
    site = Site.objects.get_current()
    site_context = {
        "site_name": site.name,
        "domain": site.domain,
        "logo_url": LOGO_URL,
    }
    return site_context