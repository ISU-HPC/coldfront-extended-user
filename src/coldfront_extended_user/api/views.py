from rest_framework.routers import APIRootView

from coldfront.api.viewsets import ColdFrontModelViewSet
from coldfront.ras import filtersets
from coldfront_extended_user.models import CustomUserFields

from . import serializers


class ExtendedUserRootView(APIRootView):
    """
    Extended User API root view
    """

    def get_view_name(self):
        return "Extended User"


class CustomUserFieldsViewSet(ColdFrontModelViewSet):
    queryset = CustomUserFields.objects.all()
    serializer_class = serializers.CustomUserFieldsSerializer