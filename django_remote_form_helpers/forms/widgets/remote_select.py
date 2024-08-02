from django import forms
from django.core.exceptions import ImproperlyConfigured
import django
if django.VERSION < (1, 10):
    from django.core.urlresolvers import reverse_lazy
else:
    from django.urls import reverse_lazy


class RemoteSelectWidget(forms.Select):
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
        if not url_name and not url:
            raise ImproperlyConfigured("Either 'url_name' or 'url' must be provided.")
        
        self.url = url if url else reverse_lazy(url_name)
        self.empty_label = empty_label
        
        attrs = attrs or {}
        attrs.update({
            'data-url': url if url else reverse_lazy(url_name),
            'data-empty-label': empty_label,
            'class': attrs.get('class', '') + ' remote-in-django-form'
        })
        
        super().__init__(*args, attrs=attrs, **kwargs)
