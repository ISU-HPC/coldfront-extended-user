from rest_framework.routers import APIRootView
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from coldfront.lib.api.viewsets import ColdFrontModelViewSet
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

    # Get custom user fields by user ID
    @action(detail=False, methods=['get'], url_path=r'user/(?P<uid>\d+)')
    def get_by_user(self, request, uid=None):
        # Query the queryset looking for the nested user__id
        custom_field_obj = get_object_or_404(self.get_queryset(), user__id=uid)
        
        # Serialize and return the object
        serializer = self.get_serializer(custom_field_obj)
        return Response(serializer.data)