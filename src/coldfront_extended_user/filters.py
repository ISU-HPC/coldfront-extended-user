from django.db.models import Q
from .models import CustomUserFields
from coldfront.views.filtersets import ColdFrontModelFilterSet

class ProjectFilterSet(ColdFrontModelFilterSet):
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