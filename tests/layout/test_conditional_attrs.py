import json

from django import forms

import pytest

from tbxforms.choices import Choice
from tbxforms.layout import (
    Div,
    Field,
    Fieldset,
    Layout,
)
from tests.forms import BaseTestForm
from tests.utils import render_form

# Field type configurations with their form field class and test values
FIELD_TYPES = {
    "checkbox": {
        "field_class": forms.BooleanField,
        "field_method": Field.checkbox,
        "trigger_values": [True],
        "kwargs": {},
    },
    "checkboxes": {
        "field_class": forms.MultipleChoiceField,
        "field_method": Field.checkboxes,
        "trigger_values": ["yes"],
        "kwargs": {
            "choices": (
                Choice("yes", "Yes"),
                Choice("no", "No"),
            ),
            "widget": forms.CheckboxSelectMultiple,
        },
    },
    "radios": {
        "field_class": forms.ChoiceField,
        "field_method": Field.radios,
        "trigger_values": ["yes"],
        "kwargs": {
            "choices": (
                Choice("yes", "Yes"),
                Choice("no", "No"),
            ),
            "widget": forms.RadioSelect,
        },
    },
    "select": {
        "field_class": forms.ChoiceField,
        "field_method": Field.select,
        "trigger_values": ["yes"],
        "kwargs": {
            "choices": (
                Choice("yes", "Yes"),
                Choice("no", "No"),
            ),
            "widget": forms.Select,
        },
    },
    "text": {
        "field_class": forms.CharField,
        "field_method": Field.text,
        "trigger_values": ["yes"],
        "kwargs": {},
    },
    "textarea": {
        "field_class": forms.CharField,
        "field_method": Field.textarea,
        "trigger_values": ["yes"],
        "kwargs": {},
    },
}


class ConditionalFormFactory:
    """
    Factory for creating form classes with different field type combinations.
    """

    @staticmethod
    def create_form(trigger_type, dependent_type):
        """
        Create a form class with specified trigger and dependent field types
        """

        class DynamicForm(BaseTestForm):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                # Add trigger field
                trigger_config = FIELD_TYPES[trigger_type]
                self.fields["trigger_field"] = trigger_config["field_class"](
                    required=True, **trigger_config["kwargs"]
                )

                # Add dependent field
                dependent_config = FIELD_TYPES[dependent_type]
                self.fields["dependent_field"] = dependent_config[
                    "field_class"
                ](required=False, **dependent_config["kwargs"])

                # Set up layout
                self.helper.layout = Layout(
                    trigger_config["field_method"]("trigger_field"),
                    dependent_config["field_method"](
                        "dependent_field",
                        data_conditional={
                            "field_name": "trigger_field",
                            "values": trigger_config["trigger_values"],
                        },
                    ),
                )

        return DynamicForm


@pytest.mark.parametrize(
    "trigger_type,dependent_type",
    [
        (trigger, dependent)
        for trigger in FIELD_TYPES.keys()
        for dependent in FIELD_TYPES.keys()
    ],
)
class TestFieldConditionals:
    """
    Test suite to ensure conditional logic can be applied to field types
    (e.g. Field.checkbox, Field.radios, etc.).
    """

    def test_conditional_attrs(self, trigger_type, dependent_type):
        """Test that conditional attributes are correctly set."""
        trigger_config = FIELD_TYPES[trigger_type]
        dependent_config = FIELD_TYPES[dependent_type]

        field = dependent_config["field_method"](
            "dependent_field",
            data_conditional={
                "field_name": "trigger_field",
                "values": trigger_config["trigger_values"],
            },
        )

        assert field.attrs["data-conditional-field-name"] == "trigger_field"
        assert (
            json.loads(field.attrs["data-conditional-field-values"])
            == trigger_config["trigger_values"]
        )

    def test_rendering(self, trigger_type, dependent_type, snapshot_html):
        """Test the HTML rendering of conditional fields."""
        Form = ConditionalFormFactory.create_form(trigger_type, dependent_type)
        form = Form()

        assert render_form(form) == snapshot_html


@pytest.mark.parametrize(
    "container_type",
    [
        ("Div", Div),
        ("Fieldset", Fieldset),
    ],
    ids=lambda x: x[0],
)
class TestContainerConditionals:
    """
    Test suite to ensure conditional logic can be applied to container types
    (e.g. Div, Fieldset).
    """

    def test_container_conditional_attrs(self, container_type, snapshot_html):
        """
        Test that conditional attributes are correctly set on containers.
        """

        container_name, container_class = container_type

        class ContainerForm(BaseTestForm):
            field1 = forms.CharField()
            field2 = forms.CharField()

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                container_kwargs = {
                    "data_conditional": {
                        "field_name": "trigger_field",
                        "values": ["yes"],
                    }
                }

                self.helper.layout = Layout(
                    container_class("field1", "field2", **container_kwargs)
                )

        form = ContainerForm()
        rendered_form = render_form(form)

        assert rendered_form == snapshot_html
        assert 'data-conditional-field-name="trigger_field"' in rendered_form
        assert (
            'data-conditional-field-values="[&quot;yes&quot;]"'
            in rendered_form
        )

    def test_container_with_multiple_values(
        self, container_type, snapshot_html
    ):
        """Test containers with multiple conditional values."""
        container_name, container_class = container_type

        class MultiValueForm(BaseTestForm):
            field1 = forms.CharField()

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                container_kwargs = {
                    "data_conditional": {
                        "field_name": "trigger_field",
                        "values": ["yes", "maybe"],
                    }
                }

                self.helper.layout = Layout(
                    container_class("field1", **container_kwargs)
                )

        form = MultiValueForm()
        rendered_form = render_form(form)

        assert rendered_form == snapshot_html
        assert (
            'data-conditional-field-values="[&quot;yes&quot;, &quot;maybe&quot;]"'  # noqa: E501
            in rendered_form
        )


@pytest.mark.parametrize(
    "field_type", [ft for ft in FIELD_TYPES.keys() if ft != "checkbox"]
)
class TestConditionalFieldsToShowAsRequiredMethod:
    """
    Test suite for the `conditional_fields_to_show_as_required` method.

    Single checkbox fields are excluded as we intentionally don't add markers
    (i.e. "(optional)" or "*") to single checkbox field labels.
    """

    @staticmethod
    def create_form(field_type):
        class DynamicForm(BaseTestForm):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                field_config = FIELD_TYPES[field_type]
                self.fields["test_field"] = field_config["field_class"](
                    required=False, **field_config["kwargs"]
                )
                self.helper.layout = Layout(
                    field_config["field_method"]("test_field")
                )

        return DynamicForm

    def test_field_can_be_shown_as_required(self, field_type, snapshot_html):
        """
        `test_field` is an optional field, but when we add it to the list
        returned by `conditional_fields_to_show_as_required`, the field should
        be shown as required.
        """

        Form = self.create_form(field_type)
        Form.conditional_fields_to_show_as_required = classmethod(
            lambda cls: ["test_field"]
        )
        form = Form()

        rendered_form = render_form(form)

        assert rendered_form == snapshot_html
        assert (
            '<span class="tbxforms-field_marker--optional">(optional)</span>'
            not in rendered_form
        )
