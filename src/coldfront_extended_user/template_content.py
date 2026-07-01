from django.urls import reverse
from .models import CustomUserFields
from coldfront.plugins import PluginTemplateExtension

import django_tables2 as tables
from django.db.models import prefetch_related_objects
from .tables import CustomUserFieldsTable

# Button for editing custom user fields
# This button only appears on the individual user view page (.../users/users/{pk})
class CustomUserFieldsButton(PluginTemplateExtension):

    model = 'users.user'

    def buttons(self):
        # The context dictionary contains the object being viewed as self.context['object']
        obj = self.context['object']
        request = self.context['request']
        current_url = request.path
        
        # Checks if current page is the individual user view page
        if current_url != reverse('users:user', kwargs={'pk': obj.pk}):
            return ""

        action_url = reverse('users:user_custom', kwargs={'pk': obj.pk})
        
        # Inject edit button into user view page
        return f"""
        <a href="{action_url}" class="btn btn-primary">
            <i class="mdi mdi-rocket"></i> Edit Custom Fields
        </a>
        """

# Right panel to display custom user fields
# This panel only appears on the individual user view page
class CustomUserFieldsPanel(PluginTemplateExtension):
    model = 'users.user'
    
    def right_page(self):
        # The context dictionary contains the object being viewed as self.context['object']
        obj = self.context['object']
        request = self.context['request']
        current_url = request.path

        # Checks if current page is the individual user view page
        is_user_page = current_url == reverse('users:user', kwargs={'pk': obj.pk})

        if not is_user_page:
            return ""
        
        # Retrieves custom user data
        custom_data, _ = CustomUserFields.objects.get_or_create(user=obj)
        
        # Inject panel into user view page
        return self.render('coldfront_extended_user/custom_fields_card.html', extra_context={
            'custom_user_fields': custom_data,
        })



# Register the extension by adding it to the template_extensions list
template_extensions = [CustomUserFieldsButton, CustomUserFieldsPanel]

