# extended_user/forms.py

from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.layout import Fieldset, Layout

from coldfront.forms.mixins import CustomAttributesMixin, CustomFieldsMixin
from coldfront.forms.model_forms import ColdFrontModelForm
from coldfront.users.forms.model_forms import UserForm

from .models import UserCustomFields
from coldfront.core.models import ObjectType
from django.contrib.auth import get_user_model
from coldfront.users import forms as core_user_forms

User = get_user_model()

class UserCustomFieldsForm(ColdFrontModelForm):

    model = UserCustomFields
    
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        disabled=True, 
        help_text="The user this custom data belongs to.",
        label=_("User"),
    )

    class Meta:
        model = UserCustomFields
        # 2. Tell the form to use the user field
        fields = [
            "user",
        ] 

    fieldsets = (
        Fieldset(
            _("User"),
            "user",
        ),
    )