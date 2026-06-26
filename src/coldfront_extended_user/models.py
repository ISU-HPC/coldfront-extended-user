from django.db import models
from django.conf import settings
from django.urls import reverse
from coldfront.models.base import BaseModel, ColdFrontModel
from coldfront.models.features import CustomFieldsMixin
from django.utils.translation import gettext_lazy as _

# Adds custom field support to a user account
# This model inherits the CustomFieldMixin instead of the core user account
class UserCustomFields(ColdFrontModel):
    
    # One-to-one mapping to core user account
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
        # Returns to core user page
        return reverse('users:user', kwargs={'pk': self.user.id})

    def __str__(self):
        return self.user.username

