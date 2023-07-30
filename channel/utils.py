import warnings

from .exceptions import ChannelNotDefined, NoDefaultChannel
from .models import Channel

DEPRECATION_WARNING_MESSAGE = (
    "Default channel used in a query. Please make sure that channel is explicitly "
    "provided."
)


def get_default_channel():
    """
    Return the default channel.
    """
    try:
        channel = Channel.objects.get()
    except Channel.MultipleObjectsReturned:
        channels = list(Channel.objects.filter(is_default=True))
        if len(channels) == 1:
            warnings.warn(DEPRECATION_WARNING_MESSAGE)
            return channels[0]
        raise ChannelNotDefined()
    except Channel.DoesNotExist:
        raise NoDefaultChannel
    else:
        warnings.warn(DEPRECATION_WARNING_MESSAGE)
        return channel
