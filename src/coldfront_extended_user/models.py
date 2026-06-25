from django.db import models
from django.conf import settings
from django.urls import reverse
from coldfront.models.base import BaseModel, ColdFrontModel
from coldfront.models.features import CustomFieldsMixin
from django.utils.translation import gettext_lazy as _

class UserCustomFields(ColdFrontModel):
    # Link this directly to the user model dynamically via settings!
    # This completely avoids all get_user_model() circular import issues.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="extended_data"
    )

    class Meta:
        ordering = ["user"]
        verbose_name = _("Custom user field")
        verbose_name_plural = _("Custom user fields")

    def get_absolute_url(self):
        # Trick NetBox into treating the parent User tab as this object's "home" URL
        return reverse('users:user', kwargs={'pk': self.user.id})

    def __str__(self):
        return self.user.username

    # Your mixin fields are now inherited here, not on the User table
