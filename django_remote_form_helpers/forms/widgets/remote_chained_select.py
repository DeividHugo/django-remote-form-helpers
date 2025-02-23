from django import forms
from django_remote_form_helpers.forms.widgets.mixins import RemoteSelectWidgetMixin


class RemoteChainedSelectWidget(forms.Select, RemoteSelectWidgetMixin):
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
        self.parent_name = parent_name
        self.url = self.get_url(url, url_name)
        self.empty_label = self.get_empty_label(empty_label)
        self.url_param_field = url_param_field or ''

        attrs = attrs or {}
        attrs.update({
            'data-parent-name': self.parent_name,
            'data-url': self.url,
            'data-empty-label': self.empty_label,
            'data-url-param-field': self.url_param_field,
            'class': attrs.get('class', '') + ' remote-chained-in-django-form'
        })
        
        super().__init__(*args, attrs=attrs, **kwargs)
