# Django Remote Form Helpers

**Documentation Version: 0.1.0**

## Overview

Django Remote Form Helpers is a library designed to enhance frontend performance and simplify dynamic data handling in Django applications. It integrates remote data sources with Django forms using AJAX-driven widgets and APIs, making complex form interactions easier to implement and manage.

### Key Benefits:

- **Faster Page Loads**: Speeds up page load times by asynchronously loading form data, reducing the need for server-side HTML generation.
- **Reduced Server Workload**: Minimizes server processing by offloading data fetching and form updates to the client side.
- **Real-Time Data Updates**: Provides dynamic updates to form fields based on user input without frequent server requests.
- **Simplified Form Handling**: Connects forms with remote APIs, simplifying Django template management.
- **Select2 Integration**: Enhances select fields with advanced features like search and multi-select, compatible with Select2.
- **Dynamic Formset Support**: Allows for dynamic addition and removal of forms directly on the frontend.

## Features

- **ModelChoicesAPIView**: A class for providing standardized choice data from a Django model via an API. It supports filtering and caching, and is designed to be used with widgets that consume API data.
- **APIFieldsHandlerFormMixin**: A mixin for validating form fields with API data and adjusting querysets dynamically based on API responses.
- **RemoteSelectWidget**: A widget that creates select fields which load their options from a remote URL using AJAX.
- **RemoteChainedSelectWidget**: A widget that creates select fields which update their options dynamically based on the selection of a parent field using AJAX.

## Installation

To install the library, run the command: `pip install django_remote_form_helpers`

## Usage

### 1. Include JavaScript

To enable frontend JavaScript functionalities, you need to include the JavaScript file in your HTML template. You can either upload the JavaScript file to your static file directory or use a CDN. 

**Note:** This script requires jQuery to function correctly. It has been tested with jQuery versions 2.1.4 through 3.6.0.

#### Option 1: Using a CDN:
If you choose to use a CDN (Content Delivery Network) to include the JavaScript file, add the following line to your HTML template:

```html
<script src="https://cdn.jsdelivr.net/gh/DeividHugo/django-remote-form-helpers/django_remote_form_helpers/static/django_remote_form_helpers/js/jquery.remote.in.django.form.js"></script>
```

**Note:** While using a CDN can be convenient for quick testing, it is not the recommended approach for production environments. For a more reliable setup, especially for production, refer to Option 2.

#### Option 2: Using Static Files in Django:

If you are serving the JavaScript file directly from your static files, you need to ensure the following:

1. **Download the File**  
   Obtain the file [jquery.remote.in.django.form.js](https://github.com/DeividHugo/django-remote-form-helpers/raw/main/django_remote_form_helpers/static/django_remote_form_helpers/js/jquery.remote.in.django.form.js).

2. **Place the File in the Static Folder**  
   - Navigate to your Django project's `static` folder. If the `static` folder does not exist, create it.
   - Place the file `jquery.remote.in.django.form.js` into the `static` folder. The structure should look like this:
     ```
     your_project/
     └── static/
         └── jquery.remote.in.django.form.js
     ```

3. **Add the Script in Your Template**  
   In your HTML template, include the following code to load the JavaScript file:
   ```html
   <script src="{% static 'jquery.remote.in.django.form.js' %}"></script>
    ```

Make sure you have Django configured to use static files and that the {% static %} tag is available. 

## 2. Creating the API

#### Option 1: Using the ModelChoicesAPIView:

The `ModelChoicesAPIView` class provides a flexible API endpoint for fetching choice data from Django models. You can configure it to use different models, value fields, and text fields.

**Example Usage with `Category` Model:**

To create an API view specifically for the `Category` model, you can subclass `ModelChoicesAPIView` and set the relevant attributes. Here’s how you can define a `CategoryModelChoicesAPIView`:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from .models import Category
from .model_choices_api_view import ModelChoicesAPIView  

class CategoryModelChoicesAPIView(ModelChoicesAPIView):
    model = Category
    value_field = 'id'  # Field used for the option value
    text_field = 'name'  # Field used for the display text
    allowed_filters = ['id', 'name']  
```

**Attributes:**

- **`model`**: Specifies the Django model to use for fetching choices. This attribute must be set to the model class you want to use.
- **`value_field`**: Defines which field in the model provides the option value (default is `'pk'`). You can set this to any field that should be used as the value for each option.
- **`text_field`**: Defines which field in the model provides the display text for each option (default is `'name'`). You can set this to any field that should be shown as the text for each option.
- **`allowed_filters`**: Determines which fields can be used to filter the queryset. By default, all fields are allowed (`'__all__'`). You can specify a list of field names to restrict filtering.

#### Option 2: Using Custom APIs

When creating a custom API endpoint, ensure that it meets the following requirements:

- **Response Format**: The API should return a JSON array where each element is an array consisting of two values:
  - The first value is the id (used as the value in the select field).
  - The second value is the text (used as the displayed text in the select field).

  **Expected Response Format:**

  ```json
  [
      [1, "First Option"],
      [2, "Second Option"]
  ]

**Important Notes:**
- **Custom Filtering**: Ensure the API supports filtering by query parameters. For `RemoteChainedSelectWidget`, the API must handle URL-based filters to update options based on the parent field’s value.

### Set URL for Custom API

**Example URL Configuration:**

In your `urls.py`, you can define a URL pattern for your custom API view:

```python
from django.urls import path
from .views import CategoryModelChoicesAPIView 

urlpatterns = [
    path('api/category-choices/', CategoryModelChoicesAPIView.as_view(), name='category_choices'),
]
```

### 3. Using `APIFieldsHandlerFormMixin`

The `APIFieldsHandlerFormMixin` provides functionality to validate form fields using API data and adjust querysets dynamically based on API responses.

#### Example Usage

```python
from django import forms
from django_remote_form_helpers.forms.mixins import APIFieldsHandlerFormMixin
from .models import Model, AnotherModel

class MyForm(APIFieldsHandlerFormMixin, forms.Form):
    field1 = forms.ModelChoiceField(queryset=Model.objects.none())
    field2 = forms.ModelChoiceField(queryset=AnotherModel.objects.all())

    API_FIELDS = ['field1']
```

In your Django form, you would use the mixin to handle fields that require validation against API data. Define the API_FIELDS attribute to specify which fields need API-based validation. For instance, you can initialize fields with empty querysets and update them based on API responses.

The APIFieldsHandlerFormMixin ensures that fields requiring API validation are handled correctly. By initializing fields with empty querysets (Model.objects.none()), any options are initially rejected. However, the mixin validates against the model and allows valid options to pass without performing heavy queries.

Thus, using the RemoteSelectWidget or RemoteChainedSelectWidget is mandatory when you need API-based validation for a field or when a field consumes API data.

### 4. Using `RemoteSelectWidget`

The `RemoteSelectWidget` is a widget that creates select fields which load their options from a remote URL using AJAX.

#### Example Usage

```python
from django import forms
from django_remote_form_helpers.forms.widgets import RemoteSelectWidget
from django_remote_form_helpers.forms.mixins import APIFieldsHandlerFormMixin
from .models import Category

class MyForm(APIFieldsHandlerFormMixin, forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        widget=RemoteSelectWidget(
            url_name='category_choices',
            empty_label='Select a category'
        )
    )

    API_FIELDS = ['category']
```

**Parameters:**

- **`url_name`**: Specifies the internal URL name for fetching data. This should be a Django URL pattern name defined in your `urls.py`.
- **`url`**: (Alternative) If you need to specify an external URL, use the `url` attribute instead of `url_name`.
- **`empty_label`**: Defines the label for the empty option in the select field. If set to `None`, no empty option will be displayed.

**Important Notes:**

- The `APIFieldsHandlerFormMixin` is **required** to handle API-based validation for fields using `RemoteSelectWidget`. Make sure to include it in your form.
- Define the `API_FIELDS` attribute in your form to list the fields that require API validation. This ensures proper handling and validation of fields that depend on dynamic data from remote sources.

### 5. Using `RemoteChainedSelectWidget`

The `RemoteChainedSelectWidget` is a widget that dynamically updates its options based on the selection of a parent field using AJAX.

#### Example Usage

In your Django form, configure a `RemoteChainedSelectWidget` for a select field that depends on the value selected in another field. Specify the parent field's name, the URL to fetch the child options, and the parameter name used to send the parent field’s value.

```python
from django import forms
from django_remote_form_helpers.forms.widgets import RemoteChainedSelectWidget
from django_remote_form_helpers.forms.mixins import APIFieldsHandlerFormMixin

class MyForm(APIFieldsHandlerFormMixin, forms.Form):
    parent_field = forms.ChoiceField(choices=[(1, 'Option 1'), (2, 'Option 2')])
    child_field = forms.ChoiceField(widget=RemoteChainedSelectWidget(
        parent_name='parent_field',
        url_name='child_choices',
        url_param_field='parent_id',
        empty_label='Select an option'
    ))

    API_FIELDS = ['child_field']
```

**Parameters:**

- **`parent_name`**: Name of the parent field that triggers updates to the child field options.
- **`url_name`**: Internal URL name for fetching data, defined in `urls.py`. Use `url` for external URLs.
- **`url`**: (Alternative) Use this for external URLs instead of `url_name`.
- **`url_param_field`**: (Optional) Name of the parameter sent to the API to filter options. Defaults to the parent field’s name if not specified.
- **`empty_label`**: Label for the empty option in the select field. If `None`, no empty option is displayed.

**Important Notes:**

- The `APIFieldsHandlerFormMixin` is **required** to handle API-based validation for fields using `RemoteSelectWidget`. Make sure to include it in your form.
- Define the `API_FIELDS` attribute in your form to list the fields that require API validation. This ensures proper handling and validation of fields that depend on dynamic data from remote sources.

## Conclusion

Django Remote Form Helpers aims to optimize form handling in Django applications by integrating remote data sources and improving user experience with AJAX-driven widgets. This project is open source, and we encourage contributions and feedback from the community. By collaborating, we can enhance the library and support a broader range of use cases, making Django development more efficient and enjoyable for everyone. 

Feel free to contribute, share your experiences, or reach out if you have any questions or suggestions!