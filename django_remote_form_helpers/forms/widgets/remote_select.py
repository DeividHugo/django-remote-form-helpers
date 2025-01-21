from django import forms
from django_remote_form_helpers.forms.widgets.mixins import RemoteSelectWidgetMixin


class RemoteSelectWidget(forms.Select, RemoteSelectWidgetMixin):
    """
    A Django form widget for creating a select field that dynamically loads its options
    from a remote URL. This widget uses AJAX to fetch the options and can display an empty
    label if no options are available.

    Example usage:
        class MyForm(APIFieldsHandlerFormMixin, forms.Form):
            category = forms.ChoiceField(widget=RemoteSelectWidget(
                url_name='api:category_list',  # The URL name for fetching category options
                empty_label='Select a category'
            ))
    """

    def __init__(self, url_name=None, url=None, empty_label='---------', *args, attrs=None, **kwargs):
        self.url = self.get_url(url, url_name)
        self.empty_label = self.get_empty_label(empty_label)
        
        attrs = attrs or {}
        attrs.update({
            'data-url': self.url,
            'data-empty-label': self.empty_label,
            'class': attrs.get('class', '') + ' remote-in-django-form'
        })
        
        super().__init__(*args, attrs=attrs, **kwargs)