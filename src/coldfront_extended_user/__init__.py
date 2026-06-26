from coldfront.plugins import PluginConfig

from .version import __version__

class ColdFrontExtendedUserConfig(PluginConfig):
    name = "coldfront_extended_user"
    verbose_name = "Coldfront Extended User"
    version = __version__
    description = "Adds the custom fields mixin to user profiles"
    author = "Trevor Zimmerman"
    author_email = "trevor04@iastate.edu"
    base_url = "coldfront_extended_user"
    min_version = "2.0.0"
    default_settings = {}

config = ColdFrontExtendedUserConfig

