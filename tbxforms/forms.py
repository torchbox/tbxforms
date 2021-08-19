from django import forms as django_forms

from wagtail.contrib.forms.forms import FormBuilder

from tbxforms.fields import DateInputField
from tbxforms.helper import FormHelper


class BaseForm:
    @staticmethod
    def conditional_fields_to_show_as_required() -> []:
        """
        Field names defined here will be shown as required fields (though they
        will not have the HTML5 required attribute).
        Actual validation of conditionally required fields will need manually
        adding via the form's `clean()` method.
        """
        return []

    class Media:
        js = ("js/tbxforms.js",)

    @property
    def helper(self):
        fh = FormHelper(self)
        fh.form_class = "tbxforms"  # Must include `tbxforms`.
        return fh


class BaseWagtailFormBuilder(FormBuilder):
    """
    Override some fields to use tbxforms functionality/variants.
    """

    def create_date_field(self, field, options):
        return DateInputField(**options)

    def create_multiselect_field(self, field, options):
        # Multiselects are difficult to use, so let's revert to checkboxes.
        options["choices"] = map(
            lambda x: (x.strip(), x.strip()), field.choices.split(",")
        )
        return django_forms.MultipleChoiceField(
            widget=django_forms.CheckboxSelectMultiple, **options
        )
