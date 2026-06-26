# views.py
from django.urls import reverse
from django.views.generic import UpdateView
from coldfront.views import ViewTab, generic
from .models import UserCustomFields
from .forms import UserCustomFieldsForm
from coldfront.users.models import User

from coldfront.registry import register_model_view
from django.utils.translation import gettext_lazy as _

@register_model_view(User, "custom")
class UserCustomFieldsView(generic.ObjectEditView):
    queryset = UserCustomFields.objects.all()
    form = UserCustomFieldsForm
    template_name = "generic/object_edit.html"

    # OPTIONAL: If you want a edit tab instead of a button, uncomment this code
    # tab = ViewTab(
    #     label=_('Edit Custom Fields'),
    #     weight=100,
    # )

    # Edit page for custom user fields
    def get_object(self, *args, **kwargs):
        user_pk = kwargs.get('pk')
        cfields, created = UserCustomFields.objects.get_or_create(user_id=user_pk)
        return cfields
    
    # Returns back to individual user view page
    def get_return_url(self, request, obj=None):
        user_pk = self.kwargs.get('pk')
        
        return reverse('users:user', kwargs={'pk': user_pk})