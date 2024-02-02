from django import forms

from tbxforms.choices import Choice
from tbxforms.fields import DateInputField
from tbxforms.forms import TbxFormsMixin
from tbxforms.layout import (
    Button,
    Field,
    Fieldset,
    Layout,
)


class ButtonForm(TbxFormsMixin, forms.Form):
    # A "([factory], [factory_args])" tuple specifies the button to display
    button_spec = (Button.primary, ("name", "Title"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            self.button_spec[0](*self.button_spec[1]),
        )


class CheckboxForm(TbxFormsMixin, forms.Form):
    accept = forms.BooleanField(
        label="I accept the terms of service",
        help_text="Please read the terms of service.",
        error_messages={"required": "You must accept our terms of service"},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field.checkbox("accept"),
        )


class CheckboxesForm(TbxFormsMixin, forms.Form):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field.checkboxes("method"),
        )


class CheckboxesChoiceForm(TbxFormsMixin, forms.Form):
    METHODS = (
        Choice("email", "Email"),
        Choice(
            "phone",
            "Phone",
            hint="Select this option only if you have a mobile phone",
        ),
        Choice("text", "Text message", divider="or"),
        Choice("none", "None of the above"),
    )

    method = forms.ChoiceField(
        choices=METHODS,
        widget=forms.CheckboxSelectMultiple,
        label="How would you like to be contacted?",
        help_text="Select all options that are relevant to you.",
        error_messages={"required": "Enter the ways to contact you"},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field.checkboxes("method"),
        )


class DateInputForm(TbxFormsMixin, forms.Form):
    date = DateInputField(
        label="When was your passport issued?",
        help_text="For example, 12 11 2007",
        require_all_fields=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field("date"),
        )


class FileUploadForm(TbxFormsMixin, forms.Form):
    file = forms.FileField(
        label="Upload a file",
        help_text="Select the CSV file to upload.",
        error_messages={
            "required": "Select the CSV file you exported from the spreadsheet"
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field("file"),
        )


class RadiosForm(TbxFormsMixin, forms.Form):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field.radios("method"),
        )


class RadiosChoiceForm(TbxFormsMixin, forms.Form):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field.radios("method"),
        )


class SelectForm(TbxFormsMixin, forms.Form):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field.select("method"),
        )


class TextInputForm(TbxFormsMixin, forms.Form):
    name = forms.CharField(
        label="Name",
        help_text="Help text",
        error_messages={"required": "Required error message"},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field.text("name"),
        )


class TextareaForm(TbxFormsMixin, forms.Form):
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea,
        help_text="Help text",
        error_messages={"required": "Required error message"},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field.textarea("description"),
        )


class FieldsetForm(TbxFormsMixin, forms.Form):
    name = forms.CharField(label="Name")
    email = forms.CharField(label="Email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Fieldset("name", "email", legend="Contact"),
        )
