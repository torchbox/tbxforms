import json

from crispy_forms import layout as crispy_forms_layout


class Layout(crispy_forms_layout.Layout):
    pass


def setup_conditional_attrs(attrs: dict):
    """
    Converts a `data_conditional` or `data-conditional` dict to two separate
    JS-friendly variables to handle conditional field/container logic.

    As an example, these examples:
        * { "data_conditional": { "field_name": "trigger_field", "values": ["yes", "no"] } }
        * { "data-conditional": { "field-name": "trigger_field", "values": ["yes", "no"] } }

    will be transformed into:
        { "data-conditional-field-name": "trigger_field", "data-conditional-field-values": "[\"yes\", \"no\"]" }
    """  # noqa: E501

    conditional_attrs = attrs.pop("data_conditional", None) or attrs.pop(
        "data-conditional", None
    )
    if conditional_attrs:
        attrs["data-conditional-field-name"] = (
            conditional_attrs["field_name"] or conditional_attrs["field-name"]
        )
        attrs["data-conditional-field-values"] = json.dumps(
            conditional_attrs["values"]
        )

    return attrs
