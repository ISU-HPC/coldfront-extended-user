from django.db.models import Q
from .models import CustomUserFields
from coldfront.lib.views.filtersets import ColdFrontModelFilterSet
from coldfront.lib.forms import ColdFrontModelFilterSetForm

class CustomUserFieldsFilterSet(ColdFrontModelFilterSet):
    class Meta:
        model = CustomUserFields
        fields = (
            "user",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(user__username__icontains=value)
        )

class CustomUserFieldsFilterSetForm(ColdFrontModelFilterSetForm):
    model = CustomUserFields