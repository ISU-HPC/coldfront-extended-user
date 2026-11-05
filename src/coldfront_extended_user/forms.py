# extended_user/forms.py

from django import forms
from django.utils.translation import gettext_lazy as _
from coldfront.lib.forms.layout import FieldSet

from coldfront.lib.forms.model_forms import ColdFrontModelForm
from coldfront.users.forms.model_forms import UserForm

from .models import CustomUserFields
from coldfront.core.models import ObjectType
from django.contrib.auth import get_user_model
from coldfront.users import forms as core_user_forms

User = get_user_model()

# Form for custom user field edit page
class CustomUserFieldsForm(ColdFrontModelForm):

    model = CustomUserFields
    
    # User field is added for reference but is NOT editable
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        disabled=True, 
        help_text="The user this custom data belongs to.",
        label=_("User"),
    )

    class Meta:
        model = CustomUserFields
        fields = [
            "user",
        ] 

    fieldsets = (
        FieldSet(
            _("User"),
            "user",
        ),
    )