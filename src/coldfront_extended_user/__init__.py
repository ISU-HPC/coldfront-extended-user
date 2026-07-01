from coldfront.plugins import PluginConfig
from django.core.checks import register

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

_columns_registered = False


# Adds custom field columns to user table after initialization
@register()
def inject_user_table_columns(app_configs, **kwargs):
    global _columns_registered
    
    # Use flag to ensure this adds columns once
    if not _columns_registered:
        from .tables import CustomUserFieldsTable
        from coldfront.users.tables import UserTable
        from coldfront.tables.utils import register_table_column 

        for c in list(CustomUserFieldsTable([]).columns):
            if c.name not in ['user', 'pk', 'id', 'actions']: 
                register_table_column(c.column, c.name, UserTable)
                
        _columns_registered = True
        
    return []
