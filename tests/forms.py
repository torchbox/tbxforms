from django import forms

from tbxforms.choices import Choice
from tbxforms.fields import DateInputField
from tbxforms.forms import BaseForm
from tbxforms.helper import FormHelper
from tbxforms.layout import (
    Fieldset,
    Layout,
)


class CheckboxForm(BaseForm, forms.Form):
    accept = forms.BooleanField(
        label="I accept the terms of service",
        help_text="Please read the terms of service.",
        error_messages={"required": "You must accept our terms of service"},
    )


class CheckboxesForm(BaseForm, forms.Form):
    method = forms.ChoiceField(
        choices=(
            ("email", "Email"),
            ("phone", "Phone"),
            ("text", "Text message"),
        ),
        widget=forms.CheckboxSelectMultiple,
        label="How would you like to be contacted?",
        help_text="Select all options that are relevant to you.",
        error_messages={"required": "Enter the ways to contact you"},
    )


class CheckboxesChoiceForm(BaseForm, forms.Form):
    METHODS = (
        Choice("email", "Email"),
        Choice(
            "phone",
            "Phone",
            hint="Select this option only if you have a mobile phone",
        ),
        Choice("text", "Text message"),
    )

    method = forms.ChoiceField(
        choices=METHODS,
        widget=forms.CheckboxSelectMultiple,
        label="How would you like to be contacted?",
        help_text="Select all options that are relevant to you.",
        error_messages={"required": "Enter the ways to contact you"},
    )


class DateInputForm(BaseForm, forms.Form):
    date = DateInputField(
        label="When was your passport issued?",
        help_text="For example, 12 11 2007",
        require_all_fields=False,
    )


class FileUploadForm(BaseForm, forms.Form):
    file = forms.FileField(
        label="Upload a file",
        help_text="Select the CSV file to upload.",
        error_messages={
            "required": "Select the CSV file you exported from the spreadsheet"
        },
    )


class RadiosForm(BaseForm, forms.Form):
    method = forms.ChoiceField(
        choices=(
            ("email", "Email"),
            ("phone", "Phone"),
            ("text", "Text message"),
        ),
        widget=forms.RadioSelect,
        label="How would you like to be contacted?",
        help_text="Select the most convenient way to contact you.",
        error_messages={"required": "Enter the best way to contact you"},
    )


class RadiosChoiceForm(BaseForm, forms.Form):
    METHODS = (
        Choice("email", "Email", hint="Do not give a work email address"),
        Choice("phone", "Phone", divider="Or"),
        Choice("text", "Text message"),
    )

    method = forms.ChoiceField(
        choices=METHODS,
        widget=forms.RadioSelect,
        label="How would you like to be contacted?",
        help_text="Select the most convenient way to contact you.",
        error_messages={"required": "Enter the best way to contact you"},
    )


class SelectForm(BaseForm, forms.Form):
    method = forms.ChoiceField(
        choices=(
            ("", "Choose"),
            ("email", "Email"),
            ("phone", "Phone"),
            ("text", "Text message"),
        ),
        widget=forms.Select,
        label="How would you like to be contacted?",
        help_text="Select the most convenient way to contact you.",
        error_messages={"required": "Enter the best way to contact you"},
    )


class TextInputForm(BaseForm, forms.Form):
    name = forms.CharField(
        label="Name",
        help_text="Help text",
        error_messages={"required": "Required error message"},
    )


class TextareaForm(BaseForm, forms.Form):
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea,
        help_text="Help text",
        error_messages={"required": "Required error message"},
    )


class FieldsetForm(BaseForm, forms.Form):
    name = forms.CharField(label="Name")
    email = forms.CharField(label="Email")

    @property
    def helper(self) -> FormHelper:
        fh = super().helper
        fh.layout = Layout(
            Fieldset("name", "email", legend="Contact"),
        )
        return fh
