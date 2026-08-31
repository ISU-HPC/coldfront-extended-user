import django_tables2 as d_tables
import logging

logger = logging.getLogger(__name__)

def run_user_table_init():
    from coldfront.users.tables import UserTable
    from .tables import CustomUserFieldsTable

    # 2. Save a reference to the original __init__ method
    original_table_init = UserTable.__init__

    # 3. Define our custom __init__ wrapper
    def user_table_init(self, *args, **kwargs):
        try:

            # django-tables2 accepts an 'extra_columns' kwarg (a list of tuples)
            extra_columns = kwargs.pop("extra_columns", [])
            if not isinstance(extra_columns, list):
                extra_columns = list(extra_columns)
            
            # Append the dynamic columns to extra_columns
            for c in list(CustomUserFieldsTable([]).columns):
                if "cf_" not in c.name: continue
                c.column.accessor = d_tables.A(f"custom_user_fields.custom_field_data.{c.name.strip('cf_')}")
                extra_columns.append((c.name, c.column))
                
            # Put the extra columns back into kwargs
            kwargs["extra_columns"] = extra_columns
            
        except Exception as e:
            # Failsafe: if the DB isn't ready (e.g. during migrations), just skip.
            logger.debug(f"Failed to load dynamic UserTable columns: {e}")

        # 4. Call the original __init__ with the modified kwargs
        original_table_init(self, *args, **kwargs)

    # 5. Apply the monkey-patch
    UserTable.__init__ = user_table_init


def run_user_filter_init():
    from coldfront.users.filtersets import UserFilterSet
    from .filters import CustomUserFieldsFilterSet
    from coldfront.users.forms import UserFilterSetForm
    from coldfront.core.models import ObjectType
    from coldfront.core.models import CustomField
    from .models import CustomUserFields

    original_filterset_init = UserFilterSet.__init__
    original_form_init = UserFilterSetForm.__init__

    try:
        from coldfront.utils.forms import FieldSet
        HAS_FIELDSET = True
    except ImportError:
        HAS_FIELDSET = False

    def user_filterset_init(self, *args, **kwargs):
        # 1. Let the original UserFilterSet initialize first (builds self.filters)
        original_filterset_init(self, *args, **kwargs)
        
        try:
            # 2. Instantiate your wrapper model's FilterSet. 
            # NetBox will dynamically query the DB right now and generate 
            # the current up-to-date cf_* filters for it.
            wrapper_filterset = CustomUserFieldsFilterSet()
            
            # 3. Steal the newly generated filters and attach them to this UserFilterSet instance
            for filter_name, filter_obj in wrapper_filterset.filters.items():
                if filter_name.startswith('cf_'):
                    print(filter_name)
                    
                    # Update the ORM lookup path to cross the one-to-one relationship
                    original_field_name = filter_obj.field_name
                    print(original_field_name)
                    filter_obj.field_name = f'custom_user_fields__{original_field_name.strip('cf_')}'
                    
                    # Inject into the current instance's filters dictionary
                    self.filters[filter_name] = filter_obj
                    
        except Exception as e:
            logger.debug(f"Failed to load dynamic User filters: {e}")

    def user_filterset_form_init(self, *args, **kwargs):
        original_form_init(self, *args, **kwargs)
        
        try:
            ot = ObjectType.objects.get_for_model(CustomUserFields)
            cfs = CustomField.objects.filter(object_types=ot)
            
            added_cf_names = []
            
            for cf in cfs:
                field_name = f'cf_{cf.name}'
                
                # Fetch the correct form field widget
                try:
                    form_field = cf.to_form_field(filter=True)
                except TypeError:
                    form_field = cf.to_form_field()
                    
                form_field.required = False 
                self.fields[field_name] = form_field
                added_cf_names.append(field_name)
                
            if added_cf_names:
                current_fieldsets = getattr(self, 'fieldsets', ())
                
                if isinstance(current_fieldsets, tuple):
                    current_fieldsets = list(current_fieldsets)
                
                cf_section_index = None
                
                # Find if a Custom Fields section already exists
                for i, fieldset in enumerate(current_fieldsets):
                    if HAS_FIELDSET and hasattr(fieldset, 'name') and fieldset.name == 'Custom Fields':
                        cf_section_index = i
                        break
                    elif not HAS_FIELDSET and isinstance(fieldset, (tuple, list)) and len(fieldset) > 0 and fieldset[0] == 'Custom Fields':
                        cf_section_index = i
                        break
                
                if cf_section_index is not None:
                    # Update existing section based on NetBox version
                    if HAS_FIELDSET:
                        existing_fields = list(current_fieldsets[cf_section_index].fields)
                        existing_fields.extend(added_cf_names)
                        current_fieldsets[cf_section_index].fields = tuple(existing_fields)
                    else:
                        existing_fields = list(current_fieldsets[cf_section_index][1])
                        existing_fields.extend(added_cf_names)
                        current_fieldsets[cf_section_index] = ('Custom Fields', tuple(existing_fields))
                else:
                    # Append a new section based on NetBox version
                    if HAS_FIELDSET:
                        # NetBox 4.x expects an instantiated FieldSet object
                        current_fieldsets.append(FieldSet(*added_cf_names, name='Custom Fields'))
                    else:
                        # NetBox 3.x expects a tuple of tuples
                        current_fieldsets.append(('Custom Fields', tuple(added_cf_names)))
                        
                # Re-save it as a strict tuple
                self.fieldsets = tuple(current_fieldsets)
                
        except Exception as e:
            logger.debug(f"Failed to load dynamic User filter form fields: {e}")
    # 4. Apply the monkey-patch
    UserFilterSet.__init__ = user_filterset_init
    UserFilterSetForm.__init__ = user_filterset_form_init