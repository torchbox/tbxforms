[![PyPI](https://img.shields.io/pypi/v/tbxforms.svg)](https://pypi.org/project/tbxforms/)
[![npm](https://img.shields.io/npm/v/tbxforms.svg)](https://www.npmjs.com/package/tbxforms) [![PyPI downloads](https://img.shields.io/pypi/dm/tbxforms.svg)](https://pypi.org/project/tbxforms/)
[![Build status](https://github.com/kbayliss/tbxforms/workflows/CI/badge.svg)](https://github.com/kbayliss/tbxforms/actions)
[![Coverage Status](https://coveralls.io/repos/github/kbayliss/tbxforms/badge.svg?branch=main)](https://coveralls.io/github/kbayliss/tbxforms?branch=main)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/kbayliss/tbxforms.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/kbayliss/tbxforms/alerts/)

# Torchbox Forms

A Torchbox-flavoured template pack for [django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms), adapted from [crispy-forms-gds](https://github.com/wildfish/crispy-forms-gds).

Out of the box, forms created with `tbxforms` will look like the
[GOV.UK Design System](https://design-system.service.gov.uk/), though many
variables can be customised.

## Contents

-   [Torchbox Forms](#torchbox-forms)
    -   [Installation](#installation)
        -   [Install the Python package](#install-the-python-package)
        -   [Install the NPM package](#install-the-npm-package)
    -   [Usage](#usage)
        -   [Create a Django form](#creating-a-django-form)
        -   [Create a Wagtail form](#creating-a-wagtail-form)
            -   [Add a `helper` property to the Wagtail form](#add-a--helper--property-to-the-wagtail-form)
            -   [Instruct a Wagtail Page model to use the newly created form](#instruct-a-wagtail-page-model-to-use-the-newly-created-form)
        -   [Render a form](#render-a-form)
        -   [Customise a form's attributes (via the `helper` property)](#customising-a-form-s-attributes--via-the--helper--property-)
            -   [Possible values for the `label_size` and `legend_size`:](#possible-values-for-the--label-size--and--legend-size--)
        -   [Conditionally-required fields](#conditionally-required-fields)
-   [Further reading](#further-reading)

## Installation

You must install both the Python package and the NPM package.

### Install the Python package

#### Install using pip

```bash
pip install tbxforms
```

#### Update/define settings

Add `django-crispy-forms` and `tbxforms` to your installed apps:

```python
INSTALLED_APPS = [
  ...
  'crispy_forms',  # django-crispy-forms
  'tbxforms',
]
```

Now add the following settings to tell `django-crispy-forms` to use `tbxforms`:

```python
CRISPY_ALLOWED_TEMPLATE_PACKS = ["tbx"]
CRISPY_TEMPLATE_PACK = "tbx"
```

### Install the NPM package

#### Install using NPM

```bash
npm install tbxforms
```

#### Instantiate your forms

```javascript
import TbxForms from 'tbxforms';

document.addEventListener('DOMContentLoaded', () => {
    for (const form of document.querySelectorAll(TbxForms.selector())) {
        new TbxForms(form);
    }
});
```

#### Import the styles into your project

...Either as CSS without any customisations:

```scss
@use 'node_modules/tbxforms/style.css';
```

...Or as Sass to customise variables:

```scss
@use 'node_modules/tbxforms/tbxforms.scss' with (
    $tbxforms-error-colour: #f00,
    $tbxforms-text-colour: #000,
);
```

Alternatively, variables can be defined in a centralised variables SCSS
such as [tbxforms/static/sass/abstracts/\_variables.scss](https://github.com/kbayliss/tbxforms/blob/main/tbxforms/static/sass/abstracts/_variables.scss).

#### Add button styles

`tbxforms` provides out-of-the-box GOV.UK Design System styles for everything
except buttons, as styles for these probably exist in your project.

You will need to write button styles for the following classes:

1. `.tbxforms-button`
2. `.tbxforms-button.tbxforms-button--primary`
3. `.tbxforms-button.tbxforms-button--secondary`
4. `.tbxforms-button.tbxforms-button--warning`

## Usage

`tbxforms` supports Django and Wagtail forms.

### Django forms

All forms must inherit from `TbxFormsBaseForm` and whichever Django base form class.

```python
from django import forms
from tbxforms.forms import BaseForm as TbxFormsBaseForm

class ExampleForm(TbxFormsBaseForm, forms.Form):
    # < Your field definitions and helper property >


class ExampleModelForm(TbxFormsBaseForm, forms.ModelForm):
    # < Your field definitions, ModelForm config, and helper property >

```

### Wagtail forms

#### Create or update a Wagtail form

Wagtail forms must inheirt from `TbxFormsBaseForm` and `WagtailBaseForm`.

```python
from wagtail.contrib.forms.forms import BaseForm as WagtailBaseForm
from tbxforms.forms import BaseForm as TbxFormsBaseForm

class ExampleWagtailForm(TbxFormsBaseForm, WagtailBaseForm):
    # < Your helper property >

```

#### Instruct a Wagtail Page model to use your form

**In your form definitions** (e.g. forms.py):

```python
from tbxforms.forms import BaseWagtailFormBuilder as TbxFormsBaseWagtailFormBuilder
from path.to.your.forms import ExampleWagtailForm

class WagtailFormBuilder(TbxFormsBaseWagtailFormBuilder):
    def get_form_class(self):
        return type(str("WagtailForm"), (ExampleWagtailForm,), self.formfields)
```

**And in your form page models** (e.g. models.py):

```python
from path.to.your.forms import WagtailFormBuilder

class ExampleFormPage(...):
    ...
    form_builder = WagtailFormBuilder
    ...
```

### Render a form

Just like Django Crispy Forms, you need to pass your form object to the
`{% crispy ... %}` template tag, e.g.:

```html
{% load crispy_forms_tags %}
<html>
    <body>
        {% crispy your_form %}
    </body>
</html>
```

### Add a submit button and customise the form via the `helper` property

Submit buttons are not automatically added - you will need to do this by
extending the form helper's `layout` (example below).

Every form that inherits from `TbxFormsBaseForm` will have the following
attributes set:

-   `html5_required = True`
-   `label_size = Size.MEDIUM`
-   `legend_size = Size.MEDIUM`
-   `form_error_title = _("There is a problem with your submission")`
-   Plus everything from [django-crispy-forms' default attributes](https://django-crispy-forms.readthedocs.io/en/latest/form_helper.html).

These can be overridden (and/or additional attributes from the above list defined)
just like you would do with any other inherited class, e.g.:

```python
from django import forms
from wagtail.contrib.forms.forms import BaseForm as WagtailBaseForm
from tbxforms.forms import BaseForm as TbxFormsBaseForm
from tbxforms.layout import Button, Size

class YourSexyForm(TbxFormsBaseForm, forms.Form):

    @property
    def helper(self):
        fh = super().helper

        # Override some settings
        fh.html5_required = False
        fh.label_size = Size.SMALL
        fh.form_error_title = _("Something's wrong, yo.")

        # Add a submit button
        fh.layout.extend([
            Button.primary(
                name="submit",
                type="submit",
                value="Submit",
            )
        ])
        return fh

```

#### Change the label and legend classes

Possible values for the `label_size` and `legend_size`:

1. `SMALL`
2. `MEDIUM` (default)
3. `LARGE`
4. `EXTRA_LARGE`

### Conditionally-required fields

`tbxforms` can show/hide parts of the `layout` depending on a given value. For
example, you could show (and require) an email address field only when the user
chooses to sign up to a newsletter (examples below).

You can apply this logic to `field`, `div`, and `fieldset` elements.

Note: any field names included within the
`conditional_fields_to_show_as_required()` method will appear on the frontend
as required, though will technically be `required=False`.

**Field example:**

```python
from django import forms
from tbxforms.choices import Choice
from tbxforms.forms import BaseForm as TbxFormsBaseForm
from tbxforms.layout import Field, Layout

class ExampleForm(TbxFormsBaseForm, forms.Form):
    NEWSLETTER_CHOICES = (
        Choice("yes", "Yes please", hint="Receive occasional email newsletters."),
        Choice("no", "No thanks"),
    )

    newsletter_signup = forms.ChoiceField(
        choices=NEWSLETTER_CHOICES
    )

    email = forms.EmailField(
        widget=forms.EmailInput(required=False)
    )

    @staticmethod
    def conditional_fields_to_show_as_required() -> [str]:
        # Non-required fields that should show as required to the user.
        return [
            "email",
        ]

    @property
    def helper(self):
        fh = super().helper

        # Override what is rendered for this form.
        fh.layout = Layout(

            # Add our newsletter sign-up field.
            Field("newsletter_signup"),

            # Add our email field and define the conditional logic.
            Field(
                "email",
                data_conditional={
                    "field_name": "newsletter_signup", # Field to inspect.
                    "values": ["yes"], # Value(s) to cause this field to show.
                },
            ),

        )

        return fh


    def clean(self):
        cleaned_data = super().clean()
        newsletter_signup = cleaned_data.get("newsletter_signup")
        email = cleaned_data.get("email")

        # Fields included within `conditional_fields_to_show_as_required()` will
        # be shown as required but not enforced - i.e. they will not have the
        # HTML5 `required` attribute set.
        # Thus we need to write our own check to enforce the value exists.
        if newsletter_signup == "yes" and not email:
            raise ValidationError(
                {
                    "email": _("This field is required."),
                }
            )
        # The tbxforms JS will attempt to clear any redundant data upon submission,
        # though it is recommended to also handle this in your clean() method.
        elif newsletter_signup == "no" and email:
            del cleaned_data['email']

        return cleaned_data

```

**Container example:**

When you have multiple fields/elements that you want to show/hide together, you
can use the exact same `data_conditional` definition as above but on a `div` or
`fieldset` element, e.g.:

```python
from tbxforms.layout import HTML, Div, Field

Layout(
    Div(
        HTML("<p>Some relevant text.</p>"),
        Field("some_other_field"),
        Field("email"),
        data_conditional={
            "field_name": "newsletter_signup",
            "values": ["yes"],
        },
    ),
)
```

# Further reading

-   Download the [PyPi package](http://pypi.python.org/pypi/tbxforms)
-   Download the [NPM package](https://www.npmjs.com/package/tbxforms)
-   Learn more about [Django Crispy Forms](https://django-crispy-forms.readthedocs.io/en/latest/)
-   Learn more about [Crispy Forms GDS](https://github.com/wildfish/crispy-forms-gds)
-   Learn more about [GOV.UK Design System](https://design-system.service.gov.uk/)
