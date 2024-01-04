from html import escape
from typing import TYPE_CHECKING

import pytest

from tbxforms.layout import Button

from .forms import ButtonForm as ButtonFormBase
from .forms import (
    CheckboxesForm,
    CheckboxForm,
    DateInputForm,
    FieldsetForm,
    FileUploadForm,
    RadiosForm,
    SelectForm,
    TextareaForm,
    TextInputForm,
)
from .utils import render_form

if TYPE_CHECKING:
    # As we support Python 3.8 we have to use `typing.*` for tuples, dicts, etc
    from typing import (
        Callable,
        Dict,
        Tuple,
        Type,
    )

    from django.forms import Form


@pytest.mark.parametrize(
    ("button_factory", "button_factory_args"),
    (
        (Button.primary, ("<i>name</i>", "<pre>Title</pre>")),
        (Button.secondary, ("<i>name</i>", "<pre>Title</pre>")),
        (Button.warning, ("<i>name</i>", "<pre>Title</pre>")),
    ),
)
def test_html_escaping_buttons(
    button_factory: "Callable",
    button_factory_args: "Tuple[str, ...]",
):
    class ButtonForm(ButtonFormBase):
        button_spec = (button_factory, button_factory_args)

    form = ButtonForm()
    rendered_form = render_form(form)

    for button_arg in button_factory_args:
        assert button_arg not in rendered_form
        button_arg_escaped = escape(button_arg)
        assert button_arg_escaped in rendered_form
        # Let's also make sure we were testing the right value:
        assert len(button_arg_escaped) > len(button_arg)


@pytest.mark.parametrize(
    ("input_form_class", "form_fields_operations"),
    (
        pytest.param(
            CheckboxForm,
            {
                "accept": {
                    "label": "<i>Accept</i>",
                    "help_text": "This is <b>mandatory</b>",
                }
            },
            id="CheckboxForm",
        ),
        pytest.param(
            CheckboxesForm,
            {
                "method": {
                    "choices": (
                        ("email", "<u>Email</u>"),
                        ("phone", "<u>Phone</u>"),
                        ("text", "<u>Text message</u>"),
                    ),
                    "label": "<i>Accept</i>",
                    "help_text": "This is <b>mandatory</b>",
                }
            },
            id="CheckboxesForm",
        ),
        pytest.param(
            DateInputForm,
            {
                "date": {
                    "label": "<i>Passport issue date</i>",
                    "help_text": "This is <b>mandatory</b>",
                }
            },
            id="DateInputForm",
        ),
        pytest.param(
            FileUploadForm,
            {
                "file": {
                    "label": "<i>Upload a file</i>",
                    "help_text": "This is <b>mandatory</b>",
                }
            },
            id="FileUploadForm",
        ),
        pytest.param(
            RadiosForm,
            {
                "method": {
                    "choices": (
                        ("email", "<u>Email</u>"),
                        ("phone", "<u>Phone</u>"),
                        ("text", "<u>Text message</u>"),
                    ),
                    "label": "<i>Accept</i>",
                    "help_text": "This is <b>mandatory</b>",
                }
            },
            id="RadiosForm",
        ),
        pytest.param(
            SelectForm,
            {
                "method": {
                    "choices": (
                        ("", "<u>Choose</u>"),
                        ("email", "<u>Email</u>"),
                        ("phone", "<u>Phone</u>"),
                        ("text", "<u>Text message</u>"),
                    ),
                    "label": "<i>Accept</i>",
                    "help_text": "This is <b>mandatory</b>",
                }
            },
            id="SelectForm",
        ),
        pytest.param(
            TextInputForm,
            {
                "name": {
                    "label": "<i>Name</i>",
                    "help_text": "This is <b>mandatory</b>",
                }
            },
            id="TextInputForm",
        ),
        pytest.param(
            TextareaForm,
            {
                "description": {
                    "label": "<i>Description</i>",
                    "help_text": "This is <b>mandatory</b>",
                }
            },
            id="TextareaForm",
        ),
        pytest.param(
            FieldsetForm,
            {
                "name": {
                    "label": "<i>Name</i>",
                    "help_text": "This is <b>mandatory</b>",
                },
                "email": {
                    "label": "<i>Email</i>",
                    "help_text": "This is <b>mandatory</b> too",
                },
            },
            id="FieldsetForm",
        ),
    ),
)
def test_html_escaping_fields(
    input_form_class: "Type[Form]",
    form_fields_operations: "Dict[str, Dict[str, str]]",
):
    form = input_form_class()
    for field_name, field_operations in form_fields_operations.items():
        for (
            field_operation_name,
            field_operation_value,
        ) in field_operations.items():
            setattr(
                form.fields[field_name],
                field_operation_name,
                field_operation_value,
            )

    rendered_form = render_form(form)

    for field_operations in form_fields_operations.values():
        for field_name, field_values in field_operations.items():
            if isinstance(field_values, tuple):
                values = field_values
            else:
                values = (field_values,)
            for value in values:
                if field_name == "choices":
                    value = value[1]
                assert value not in rendered_form
                value_escaped = escape(value)
                assert value_escaped in rendered_form
                # Let's also make sure we were testing the right value:
                assert len(value_escaped) > len(value)
