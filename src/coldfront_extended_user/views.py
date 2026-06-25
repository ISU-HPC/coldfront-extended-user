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

    # tab = ViewTab(
    #     label=_('Edit Custom Fields'),
    #     weight=100,
    # )

    def get_object(self, *args, **kwargs):
        user_pk = kwargs.get('pk')
        print(user_pk)
        cfields, created = UserCustomFields.objects.get_or_create(user_id=user_pk)
        return cfields
    
    def get_return_url(self, request, obj=None):
        user_pk = self.kwargs.get('pk')
        
        # For NetBox v3.x (Standard Django User model)
        return reverse('users:user', kwargs={'pk': user_pk})