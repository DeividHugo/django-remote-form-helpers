from django import forms


class APIFieldsHandlerFormMixin:
    """
    Django form mixin for validating fields using API data.

    Uses a list of specific fields defined in API_FIELDS to validate
    if the values received via API exist in the database. If the initial
    queryset for a ModelChoiceField is None, the mixin dynamically adjusts
    it based on API data to authorize values that exist in the database.

    Example usage:
        class MyForm(APIFieldsHandlerFormMixin, forms.Form):
            API_FIELDS = ['field1']

            field1 = forms.ModelChoiceField(queryset=Model.objects.none())  # Initial queryset is None
            field2 = forms.ModelChoiceField(queryset=AnotherModel.objects.all())

            # Other form fields...

    Attributes:
        API_FIELDS (list): List of form field names to validate using API data.
    """
    API_FIELDS = [] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.API_FIELDS:
            self.initialize_api_fields()
            self.update_api_fields_on_bound()

    def initialize_api_fields(self):
        if not self.is_bound:
            for field_name in self.API_FIELDS:
                form_field = self.fields.get(field_name)
                initial_value = self.initial.get(field_name, None)
                
                if isinstance(form_field, forms.ModelChoiceField):                
                    if initial_value is None and self.instance:
                        initial_value = getattr(self.instance, field_name, None)
                    
                    if initial_value is not None:
                        model_class = form_field.queryset.model
                        queryset = ( 
                            model_class.objects.filter(pk=initial_value.pk)
                            if  isinstance(initial_value, model_class) else
                            model_class.objects.filter(pk=initial_value)
                        )
                        form_field.queryset = queryset

    def update_api_fields_on_bound(self):
        if self.is_bound:
            for field_name in self.API_FIELDS:
                form_field = self.fields.get(field_name)
                if isinstance(form_field, forms.ModelChoiceField):
                    prefixed_name = self.add_prefix(field_name)
                    api_value = self.data.get(prefixed_name)
                    model = form_field.queryset.model
                    if api_value:
                        form_field.queryset = model.objects.filter(pk=api_value)

    def add_prefix(self, field_name):
        if self.prefix:
            return f"{self.prefix}-{field_name}"
        return field_name