import django_tables2 as tables
from django.utils.translation import gettext_lazy as _
from coldfront.tables import ColdFrontTable

from .models import CustomUserFields

class CustomUserFieldsTable(ColdFrontTable):
    user = tables.Column(
        verbose_name=_("User"),
        linkify=True,
    )

    class Meta(ColdFrontTable.Meta):
        model = CustomUserFields
        fields = (
            "user",
        )

        default_columns = ()

# for c in list(CustomUserFieldsTable([]).columns):
#     if c.name in ['user', 'pk', 'id', 'actions']: continue

#     register_table_column(c.column, c.name, UserTable)
