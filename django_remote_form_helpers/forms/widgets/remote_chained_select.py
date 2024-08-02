from django import forms
from django.core.exceptions import ImproperlyConfigured
import django
if django.VERSION < (1, 10):
    from django.core.urlresolvers import reverse_lazy
else:
    from django.urls import reverse_lazy


class RemoteChainedSelectWidget(forms.Select):
    """
    A Django form widget for creating a select field that dynamically updates its options
    based on the selection of a parent field. This widget uses AJAX requests to fetch the
    options from the server and update the field.

    Example usage:
        class MyForm(APIFieldsHandlerFormMixin, forms.Form):
            parent_field = forms.ChoiceField(choices=[(1, 'Option 1'), (2, 'Option 2')])
            child_field = forms.ChoiceField(widget=RemoteChainedSelectWidget(
                parent_input_attr_name='parent_field',
                url_name='api:child_options',
                url_param_field='parent_id',
                empty_label='Select an option'
            ))
    """
    def __init__(self, parent_name, url_name=None, url=None, url_param_field=None, empty_label='---------', *args, attrs=None, **kwargs):
        if not url_name and not url:
            raise ImproperlyConfigured("Either 'url_name' or 'url' must be provided.")
        
        attrs = attrs or {}
        attrs.update({
            'data-parent-name': parent_name,
            'data-url': url if url else reverse_lazy(url_name),
            'data-empty-label': empty_label,
            'data-url-param-field': url_param_field or '',
            'class': attrs.get('class', '') + ' remote-chained-in-django-form'
        })
        
        super().__init__(*args, attrs=attrs, **kwargs)
