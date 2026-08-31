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

    def ready(self):
        super().ready()


        from .init_overrides import run_user_table_init, run_user_filter_init
        run_user_table_init()
        # run_user_filter_init()


config = ColdFrontExtendedUserConfig

_columns_registered = False


# # Adds custom field columns to user table after initialization
# @register()
# def inject_user_table_columns(app_configs, **kwargs):
#     global _columns_registered

#     print("IM RUNNING")
    
#     # Use flag to ensure this adds columns once
#     if not _columns_registered:
#         from .tables import CustomUserFieldsTable
#         from coldfront.users.tables import UserTable
#         from coldfront.tables.utils import register_table_column 

#         for c in list(CustomUserFieldsTable([]).columns):
#             if "cf_" not in c.name: 
#                 c.column.accessor = d_tables.A(f"custom_user_fields.custom_field_data.{c.name.strip('cf_')}")
#                 register_table_column(c.column, c.name, UserTable)
#                 # print(c.name)
                
#         _columns_registered = True
        
#     return []
