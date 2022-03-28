from django import forms as django_forms
from django.apps import apps
from django.conf import settings
from django.utils.html import conditional_escape

from tbxforms.fields import DateInputField
from tbxforms.helper import FormHelper
from tbxforms.layout import Size

if apps.is_installed("wagtail.contrib.forms"):
    from wagtail.contrib.forms.forms import FormBuilder


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

    @property
    def helper(self) -> FormHelper:
        fh = FormHelper(self)
        fh.form_class = "tbxforms"  # Must include `tbxforms`.

        # Define some defaults.
        fh.html5_required = True
        fh.label_size = Size.MEDIUM
        fh.legend_size = Size.MEDIUM
        return fh

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Escape HTML within `label` and `help_text` unless it's set to allow.
        # NB. Also see https://github.com/torchbox/tbxforms/blob/main/tbxforms/layout/buttons.py#L102  # noqa: E501
        for field_name, field in self.fields.items():
            if all(
                [
                    field.label,
                    not getattr(settings, "TBXFORMS_ALLOW_HTML_LABEL", False),
                ]
            ):
                field.label = conditional_escape(field.label)

            if all(
                [
                    field.help_text,
                    not getattr(
                        settings, "TBXFORMS_ALLOW_HTML_HELP_TEXT", False
                    ),
                ]
            ):
                field.help_text = conditional_escape(field.help_text)


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
