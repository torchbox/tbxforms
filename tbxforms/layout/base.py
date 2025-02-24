import json

from crispy_forms import layout as crispy_forms_layout


class Layout(crispy_forms_layout.Layout):
    pass


def setup_conditional_attrs(kwargs: dict):
    """
    Set up our flat attributes to handle conditional field/container logic.

    As an example, this will transform:
        { "data_conditional": { "field_name": "trigger_field", "values": ["yes", "no"] } }
    to:
        { "data_conditional_field_name": "trigger_field", "data_conditional_field_values": "[\"yes\", \"no\"]" }
    """  # noqa: E501

    conditional_attrs = kwargs.pop("data_conditional", None)
    if conditional_attrs:
        kwargs["data_conditional_field_name"] = conditional_attrs["field_name"]
        kwargs["data_conditional_field_values"] = json.dumps(
            conditional_attrs["values"]
        )

    return kwargs
