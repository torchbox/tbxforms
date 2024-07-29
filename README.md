[![PyPI](https://img.shields.io/pypi/v/tbxforms.svg)](https://pypi.org/project/tbxforms/)
[![npm](https://img.shields.io/npm/v/tbxforms.svg)](https://www.npmjs.com/package/tbxforms) [![PyPI downloads](https://img.shields.io/pypi/dm/tbxforms.svg)](https://pypi.org/project/tbxforms/) [![CI](https://github.com/torchbox/tbxforms/actions/workflows/test.yml/badge.svg)](https://github.com/torchbox/tbxforms/actions/workflows/test.yml)

# Torchbox Forms

A Torchbox-flavoured template pack for [django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms), adapted from [crispy-forms-gds](https://github.com/wildfish/crispy-forms-gds).

Out of the box, forms created with `tbxforms` will look like the
[GOV.UK Design System](https://design-system.service.gov.uk/), though many
variables can be customised.

## Requirements

-   python `>=3.8.1,<4.0`
-   Django `>=3.2`
-   django-crispy-forms `>=2.1,<3.0`
-   wagtail `>=2.15` if using `WagtailBaseForm`
-   sass `>=1.33.0` if building the sass yourself

<!-- prettier-ignore-start -->
> [!NOTE]
> **[govuk-frontend](https://github.com/alphagov/govuk-frontend) will
> not, and does not need to, be installed to use this package.**
>
> All form-related styles from `govuk-frontend==5.4.1` have been
> copied into this project with the prepended "govuk-" replaced with
> "tbxforms-", e.g. `.govuk-button` to `.tbxforms-button` and
> `@mixin govuk-clearfix` to `@mixin tbxforms-clearfix`.
<!-- prettier-ignore-end -->

For non-government projects, installing the complete GOV.UK Frontend package
unnecessarily increases the bundle size as we only need form-related styles.

For government projects, this increases the bundle size as both `tbxforms` and
`govuk-frontend` must be installed. However, these projects are less common, so
they are not prioritised.

## Installation

You must install both the Python package and the NPM package.

### Install the Python package

Install using pip:

```bash
pip install tbxforms
```

Add `django-crispy-forms` and `tbxforms` to your installed apps:

```python
INSTALLED_APPS = [
  # ...
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

Install using NPM:

```bash
npm install tbxforms
```

Note: This package uses the `Element.closest`, `NodeList.forEach`, and
`Array.includes` APIs. You will need to install and configure polyfills for
legacy browser support if you need to.

Instantiate your forms:

```javascript
import TbxForms from 'tbxforms';

document.addEventListener('DOMContentLoaded', () => {
    for (const form of document.querySelectorAll(TbxForms.selector())) {
        new TbxForms(form);
    }
});
```

Import the styles into your project...

...Either as CSS without any customisations:

```scss
@use 'node_modules/tbxforms/dist/style.css';
```

...Or as Sass to customise variables:

```scss
@use 'node_modules/tbxforms/tbxforms.scss' with (
    $tbxforms-text-colour: #000,
    $tbxforms-error-colour: #f00,
);
```

#### Add button styles

`tbxforms` provides out-of-the-box GOV.UK Design System styles for everything
except buttons, as styles for these probably exist within your project.

You will need to write button styles for the following classes:

1. `.tbxforms-button`
2. `.tbxforms-button.tbxforms-button--primary`
3. `.tbxforms-button.tbxforms-button--secondary`
4. `.tbxforms-button.tbxforms-button--warning`

## Usage

`tbxforms` can be used for coded Django forms and editor-controlled Wagtail forms.

### Django forms

All forms must inherit the `TbxFormsMixin` mixin, as well as specifying a Django base form class (e.g. `forms.Form` or `forms.ModelForm`)

```python
from django import forms
from tbxforms.forms import TbxFormsMixin

class ExampleForm(TbxFormsMixin, forms.Form):
    ...

class ExampleModelForm(TbxFormsMixin, forms.ModelForm):
    ...
```

### Wagtail forms

#### Create or update a Wagtail form

Wagtail forms must inherit from `TbxFormsMixin` and `WagtailBaseForm`.

```python
from wagtail.contrib.forms.forms import BaseForm as WagtailBaseForm
from tbxforms.forms import TbxFormsMixin

class ExampleWagtailForm(TbxFormsMixin, WagtailBaseForm):
    ...
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
        {% crispy your_sexy_form %}
    </body>
</html>
```

### `FormHelper`s

A [FormHelper](https://django-crispy-forms.readthedocs.io/en/latest/form_helper.html)
allows you to alter the rendering behaviour of forms.

Every form that inherits from `TbxFormsMixin` (i.e. every form within `tbxforms`)
will have a `FormHelper` with the following default attributes:

-   `html5_required = True`
-   `label_size = Size.MEDIUM`
-   `legend_size = Size.MEDIUM`
-   `form_error_title = _("There is a problem with your submission")`
-   Plus everything from [django-crispy-forms' default attributes](https://django-crispy-forms.readthedocs.io/en/latest/form_helper.html).

These can be changed during instantiation or [on the go](https://django-crispy-forms.readthedocs.io/en/latest/dynamic_layouts.html) - examples below.

#### Add a submit button

Submit buttons are not automatically added to forms. To add one, you can extend
the `form.helper.layout` (examples below).

Extend during instantiation:

```python
from django import forms
from tbxforms.forms import TbxFormsMixin
from tbxforms.layout import Button

class YourSexyForm(TbxFormsMixin, forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout.extend([
            Button.primary(
                name="submit",
                type="submit",
                value="Submit",
            )
        ])
```

Or afterwards:

```python
from tbxforms.layout import Button

form = YourSexyForm()
form.helper.layout.extend([
    Button.primary(
        name="submit",
        type="submit",
        value="Submit",
    )
])
```

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
from django.core.exceptions import ValidationError
from tbxforms.choices import Choice
from tbxforms.forms import TbxFormsMixin
from tbxforms.layout import Field, Layout

class ExampleForm(TbxFormsMixin, forms.Form):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            # Add our newsletter sign-up field.
            Field.text("newsletter_signup"),

            # Add our email field and define the conditional logic.
            Field.text(
                "email",
                data_conditional={
                    "field_name": "newsletter_signup", # Field to inspect.
                    "values": ["yes"], # Value(s) to cause this field to show.
                },
            ),
        )

    @staticmethod
    def conditional_fields_to_show_as_required() -> [str]:
        # Non-required fields that should show as required to the user.
        return [
            "email",
        ]

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
                    "email": "This field is required.",
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
from tbxforms.layout import HTML, Div, Field, Layout

Layout(
    Div(
        HTML("<p>Some relevant text.</p>"),
        Field.text("some_other_field"),
        Field.text("email"),
        data_conditional={
            "field_name": "newsletter_signup",
            "values": ["yes"],
        },
    ),
)
```

## Customising behaviour

### Highlight required fields instead of optional ones

If `TBXFORMS_HIGHLIGHT_REQUIRED_FIELDS=False` (or unset), optional fields will
have "(optional)" appended to their labels. This is the default behaviour and
recommended by GDS.

If `TBXFORMS_HIGHLIGHT_REQUIRED_FIELDS=True`, required fields will have an
asterisk appended to their labels and optional fields will not be highlighted.

You can also style these markers by targeting these CSS classes:

-   `.tbxforms-field_marker--required`
-   `.tbxforms-field_marker--optional`

### Change the default label and legend classes

Possible values for the `label_size` and `legend_size`:

1. `SMALL`
2. `MEDIUM` (default)
3. `LARGE`
4. `EXTRA_LARGE`

# Further reading

-   Download the [PyPI package](http://pypi.python.org/pypi/tbxforms)
-   Download the [NPM package](https://www.npmjs.com/package/tbxforms)
-   Learn more about [Django Crispy Forms](https://django-crispy-forms.readthedocs.io/en/latest/)
-   Learn more about [Crispy Forms GDS](https://github.com/wildfish/crispy-forms-gds)
-   Learn more about [GOV.UK Design System](https://design-system.service.gov.uk/)
