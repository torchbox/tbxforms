from django import forms as django_forms
from django.apps import apps

from tbxforms.fields import DateInputField
from tbxforms.helper import FormHelper
from tbxforms.layout import Size

if apps.is_installed("wagtail.contrib.forms"):
    from wagtail.contrib.forms.forms import FormBuilder


class TbxFormsMixin:
    @staticmethod
    def conditional_fields_to_show_as_required() -> []:
        """
        Field names defined here will be shown as required fields (though they
        will not have the HTML5 required attribute).
        Actual validation of conditionally required fields will need manually
        adding via the form's `clean()` method.
        """
        return []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = "tbxforms"  # "form.tbxforms" is used by our JS to add conditional field logic.  # noqa: E501
        self.helper.html5_required = True
        self.helper.label_size = Size.MEDIUM
        self.helper.legend_size = Size.MEDIUM


if "FormBuilder" in locals():

    class BaseWagtailFormBuilder(FormBuilder):
        """
        Override some fields to use tbxforms functionality/variants.
        """

        def create_date_field(self, field, options) -> DateInputField:
            return DateInputField(**options)

        def create_multiselect_field(
            self, field, options
        ) -> django_forms.MultipleChoiceField:
            # Multiselects are difficult to use, so let's revert to checkboxes.
            options["choices"] = map(
                lambda x: (x.strip(), x.strip()), field.choices.split(",")
            )
            return django_forms.MultipleChoiceField(
                widget=django_forms.CheckboxSelectMultiple, **options
            )
