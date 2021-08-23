# Torchbox Forms

[![PyPI](https://img.shields.io/pypi/v/tbxforms.svg)](https://pypi.org/project/tbxforms/) [![npm](https://img.shields.io/npm/v/tbxforms.svg)](https://www.npmjs.com/package/tbxforms) [![PyPI downloads](https://img.shields.io/pypi/dm/tbxforms.svg)](https://pypi.org/project/tbxforms/) [![Build status](https://github.com/torchbox/tbxforms/workflows/CI/badge.svg)](https://github.com/torchbox/tbxforms/actions) [![Coverage Status](https://coveralls.io/repos/github/torchbox/tbxforms/badge.svg?branch=main)](https://coveralls.io/github/torchbox/tbxforms?branch=main) [![Total alerts](https://img.shields.io/lgtm/alerts/g/torchbox/tbxforms.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/torchbox/tbxforms/alerts/)

A Torchbox-flavoured template pack for [django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms), based on [crispy-forms-gds](https://github.com/wildfish/crispy-forms-gds).

## Installation

Use of this package requires you to install both a Python package and an NPM package.

### Install the Python package

Install using pip:

```bash
pip install tbxforms
```

Add `django-crispy-forms` and `tbxforms` to your installed apps:

```python
INSTALLED_APPS = [
  ...
  'crispy_forms',  # django-crispy-forms
  'tbxforms',
]
```

Now add the following settings to tell `django-crispy-forms` to use this theme:

```python
CRISPY_ALLOWED_TEMPLATE_PACKS = ["tbx"]
CRISPY_TEMPLATE_PACK = "tbx"
```

### Install the NPM package

TODO.

Include instructions for:

-   SCSS
-   JS

## Usage

### Creating a Django form

```python
from tbxforms.forms import BaseForm as TbxFormsBaseForm

class ExampleForm(TbxFormsBaseForm, forms.Form):
    # < Your field definitions >

    # Although not required, it is recommended to add a helper:
    @property
    def helper(self):
        fh = super().helper
        fh.html5_required = True
        fh.label_size = Size.MEDIUM
        fh.legend_size = Size.MEDIUM
        fh.form_error_title = _("There is a problem with your submission")
        return fh

class ExampleModelForm(TbxFormsBaseForm, forms.ModelForm):
    # < Your field definitions and ModelForm config >

    # Although not required, it is recommended to add a helper:
    @property
    def helper(self):
        fh = super().helper
        fh.html5_required = True
        fh.label_size = Size.MEDIUM
        fh.legend_size = Size.MEDIUM
        fh.form_error_title = _("There is a problem with your submission")
        return fh
```

### Creating a Wagtail form

Two parts are required for this to work:

1. Add a `helper` property to the Wagtail form
2. Instruct a Wagtail Page model to use the newly created form

#### Add a `helper` property to the Wagtail form

```python
from wagtail.contrib.forms.forms import BaseForm as WagtailBaseForm

class ExampleWagtailForm(WagtailBaseForm):
    @property
    def helper(self):
        fh = super().helper
        fh.html5_required = True
        fh.label_size = Size.MEDIUM
        fh.legend_size = Size.MEDIUM
        fh.form_error_title = _("There is a problem with your submission")
        fh.add_input(
            Button.primary(
                name="submit",
                type="submit",
                value=_("Submit"),
            )
        )
        return fh
```

#### Instruct a Wagtail Page model to use the newly created form

```python
# in your forms definitions (e.g. forms.py)

from tbxforms.forms import BaseWagtailFormBuilder as TbxFormsWagtailFormBuilder

class WagtailFormBuilder(TbxFormsWagtailFormBuilder):
    def get_form_class(self):
        return type(str("WagtailForm"), (ExampleWagtailForm,), self.formfields)

# in your page models (e.g. models.py)

from path.to.your.forms import WagtailFormBuilder

class ExampleFormPage(YourPageAncestors):
    ...
    form_builder = WagtailFormBuilder
    ...
```

### Rendering a form on the frontend

Simply pass your form to the `{% crispy .. %}` template tag using the Context.

e.g. (where `name_of_your_form_variable` is the key you've chosen to add your form to the Context):

```html
{% load crispy_forms_tags %} {% crispy name_of_your_form_variable %}
```

# Further reading

-   Download the `PyPi package`\_
-   Download the `NPM package`\_
-   Learn more about `Django Crispy Forms`\_
-   Learn more about `Crispy Forms GDS`\_

.. \_PyPi package: http://pypi.python.org/pypi/tbxforms
.. \_NPM package: https://www.npmjs.com/package/tbxforms
.. \_Django Crispy Forms: https://django-crispy-forms.readthedocs.io/en/latest/
.. \_Crispy Forms GDS: https://github.com/wildfish/crispy-forms-gds
