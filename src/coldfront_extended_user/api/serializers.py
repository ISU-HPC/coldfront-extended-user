from coldfront.api.serializers import (
    PrimaryModelSerializer,
)

from coldfront.users.api.serializers import UserSerializer
from coldfront_extended_user.models import CustomUserFields


class CustomUserFieldsSerializer(PrimaryModelSerializer):
    user = UserSerializer(nested=True)

    class Meta:
        model = CustomUserFields
        fields = [
            "id",
            "user",
            "custom_fields",
        ]
        brief_fields = ("id", "username")