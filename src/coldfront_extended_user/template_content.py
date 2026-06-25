from django.urls import reverse
from .models import UserCustomFields
from coldfront.plugins import PluginTemplateExtension

class UserCustomFieldsButton(PluginTemplateExtension):
    # Specify the app_label.model_name this extension applies to
    model = 'users.user'

    def buttons(self):
        # The context dictionary contains the object being viewed as self.context['object']
        obj = self.context['object']
        request = self.context['request']
        current_url = request.path

        # print(current_url)
        # print(reverse('users:user', kwargs={'pk': obj.pk}))

        if current_url != reverse('users:user', kwargs={'pk': obj.pk}):
            return ""

        action_url = reverse('users:user_custom', kwargs={'pk': obj.pk})
        
        # Return the HTML string for your button
        # Netbox uses Bootstrap 5 and Material Design Icons (mdi)
        return f"""
        <a href="{action_url}" class="btn btn-primary">
            <i class="mdi mdi-rocket"></i> Edit Custom Fields
        </a>
        """
    
class UserCustomFieldsPanel(PluginTemplateExtension):
    model = 'users.user'
    
    def right_page(self):
        # The context dictionary contains the object being viewed as self.context['object']
        obj = self.context['object']
        request = self.context['request']
        current_url = request.path

        custom_data, _ = UserCustomFields.objects.get_or_create(user=obj)

        # print(current_url)
        # print(reverse('users:user', kwargs={'pk': obj.pk}))

        if current_url != reverse('users:user', kwargs={'pk': obj.pk}):
            return ""
        

        return self.render('coldfront_extended_user/custom_fields_card.html', extra_context={
            'extended_data': custom_data,
        })

# Register the extension by adding it to the template_extensions list
template_extensions = [UserCustomFieldsButton, UserCustomFieldsPanel]