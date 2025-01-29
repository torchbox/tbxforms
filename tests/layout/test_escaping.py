from html import escape
from typing import TYPE_CHECKING

from django.utils.html import mark_safe

import pytest

from tbxforms.layout import Button
from tests.forms import (
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
from tests.utils import (
    render_form,
    render_template,
)

if TYPE_CHECKING:
    # As we support Python 3.8 we have to use `typing.*` for tuples, dicts, etc
    from typing import (
        Dict,
        Type,
    )

    from django.forms import Form


@pytest.mark.parametrize(
    ("button_factory"),
    (
        (Button.primary),
        (Button.secondary),
        (Button.warning),
    ),
)
class TestButtonEscaping:
    """
    Suite of tests for buttons to ensure values are escaped by default but can
    be marked as safe.
    """

    TEMPLATE = '{% include "tbxforms/layout/button.html" %}'

    def test_unsafe_markup_escaped(self, button_factory, snapshot_html):
        """
        Assert unsafe markup is escaped by default.
        """

        button = button_factory(name="name", value="<strong>Value</strong>")
        result = render_template(self.TEMPLATE, input=button)

        assert result == snapshot_html
        assert escape("<strong>Value</strong>") in result
        assert "<strong>Value</strong>" not in result

    def test_safe_markup_rendered(self, button_factory, snapshot_html):
        """
        Assert safe markup is rendered.
        """

        button = button_factory(
            name="name", value=mark_safe("<strong>Value</strong>")
        )
        result = render_template(self.TEMPLATE, input=button)

        assert result == snapshot_html
        assert escape("<strong>Value</strong>") not in result
        assert "<strong>Value</strong>" in result


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
        ),
        pytest.param(
            DateInputForm,
            {
                "date": {
                    "label": "<i>Passport issue date</i>",
                    "help_text": "This is <b>mandatory</b>",
                }
            },
        ),
        pytest.param(
            FileUploadForm,
            {
                "file": {
                    "label": "<i>Upload a file</i>",
                    "help_text": "This is <b>mandatory</b>",
                }
            },
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
        ),
        pytest.param(
            TextInputForm,
            {
                "name": {
                    "label": "<i>Name</i>",
                    "help_text": "This is <b>mandatory</b>",
                }
            },
        ),
        pytest.param(
            TextareaForm,
            {
                "description": {
                    "label": "<i>Description</i>",
                    "help_text": "This is <b>mandatory</b>",
                }
            },
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
        ),
    ),
)
class TestFieldEscaping:
    """
    Suite of tests for fields that aren't buttons to ensure values are
    escaped by default but can be marked as safe.
    """

    def test_unsafe_markup_escaped(
        self,
        input_form_class: "Type[Form]",
        form_fields_operations: "Dict[str, Dict[str, str]]",
    ):
        """
        Assert unsafe markup is escaped by default.
        """

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

    def test_safe_markup_rendered(
        self,
        input_form_class: "Type[Form]",
        form_fields_operations: "Dict[str, Dict[str, str]]",
    ):
        """
        Assert safe markup is rendered.
        """

        form = input_form_class()
        for field_name, field_operations in form_fields_operations.items():
            for (
                field_operation_name,
                field_operation_value,
            ) in field_operations.items():
                if isinstance(field_operation_value, tuple):
                    """
                    If working with a tuple, apply mark_safe() to the tuples
                    values.
                    """

                    _field_operation_values = tuple()

                    for key, value in field_operation_value:
                        _field_operation_values = (
                            *_field_operation_values,
                            (key if key else "", mark_safe(value)),
                        )

                    setattr(
                        form.fields[field_name],
                        field_operation_name,
                        _field_operation_values,
                    )

                else:
                    """
                    If not working with a tuple, apply mark_safe() to the
                    value.
                    """

                    setattr(
                        form.fields[field_name],
                        field_operation_name,
                        mark_safe(field_operation_value),
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

                    assert value in rendered_form

                    value_escaped = escape(value)
                    assert value_escaped not in rendered_form
