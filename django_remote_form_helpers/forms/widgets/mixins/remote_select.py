from django.core.exceptions import ImproperlyConfigured
import django
if django.VERSION < (1, 10):
    from django.core.urlresolvers import reverse_lazy
else:
    from django.urls import reverse_lazy


class RemoteSelectWidgetMixin:

    def get_url(self, url, url_name):
        if not url and not url_name:
            raise ImproperlyConfigured("Either 'url_name' or 'url' must be provided.")
        return url if url else reverse_lazy(url_name)

    def get_empty_label(self, empty_label):
        if empty_label is None:
            return ''
        return empty_label
