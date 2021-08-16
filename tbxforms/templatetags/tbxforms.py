import ast
import html
import json

from django import (
    forms,
    template,
)
from django.conf import settings

from crispy_forms.utils import TEMPLATE_PACK

register = template.Library()


@register.filter
def show_as_required(boundfield):
    """
    Shows fields that are conditionally required (i.e. fields that do not have
    the HTML 'required' flag, as they become 'required' via the clean method
    due to another action, such as selecting "Other" on a series of radio
    buttons) as required.
    """
    if any(
        [
            boundfield.field.required,
            boundfield.name
            in boundfield.form.conditional_fields_to_show_as_required(),
        ]
    ):
        return True
    return False


@register.filter
def dict_pop(d, key):
    """
    Template filter that looks removes a key-value pair from a dict.
    """
    return d.pop(key)


@register.filter
def field_errors(bound_field):
    """
    Template tag that returns the set of errors indexed by field id.

    Each key-value pair in the dict is the id of the field and the
    list of errors for that field. The items are returned rather than
    the dict to get over a limitation in the template syntax.

    """
    seen = []
    errors = {}
    if hasattr(bound_field.field, "fields"):
        for idx, subfield in enumerate(bound_field.field.fields):
            key = "%s_%d" % (bound_field.auto_id, idx)
            subfield_errors = getattr(subfield.widget, "errors", [])
            errors[key] = subfield_errors
            seen.extend(subfield_errors)
    for error in bound_field.errors:
        if error not in seen:
            errors.setdefault(bound_field.auto_id, [])
            errors[bound_field.auto_id].append(error)
    return errors.items()


@register.filter
def is_checkbox(field):
    """
    Template filter that returns True if the field is a checkbox, False otherwise.
    """
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter
def is_radios(field):
    """
    Template filter that returns True if the field is a set of radio
    buttons field, False otherwise.
    """
    return isinstance(field.field.widget, forms.RadioSelect)


@register.filter
def is_select(field):
    """
    Template filter that returns True if the field is a drop-down select
    field, False otherwise.
    """
    return isinstance(field.field.widget, forms.Select)


@register.filter
def is_checkboxes(field):
    """
    Template filter that returns True if the field is set of checkboxes,
    False otherwise.
    """
    return isinstance(field.field.widget, forms.CheckboxSelectMultiple)


@register.filter
def is_file(field):
    """
    Template filter that returns True if the field is a file upload button,
    False otherwise.
    """
    return isinstance(field.field.widget, forms.FileInput)


@register.filter
def is_multivalue(field):
    """
    Template filter that returns True if the field is a multi-value field,
    False otherwise.
    """
    return isinstance(field.field.widget, forms.MultiWidget)


def pairwise(iterable):
    """
    Splits a list of items into pairs: s -> (s0,s1), (s2,s3), (s4, s5), ...
    """
    a = iter(iterable)
    return zip(a, a)


class CrispyGDSFieldNode(template.Node):
    """
    The TemplateNode used for rendering a field from the template pack.
    """

    def __init__(self, field, attrs):
        self.field = field
        self.attrs = attrs
        self.html5_required = "html5_required"

    def render(self, context):  # noqa: C901
        # Nodes are not threadsafe so we must store and look up our instance
        # variables in the current rendering context first
        if self not in context.render_context:
            context.render_context[self] = (
                template.Variable(self.field),
                self.attrs,
                template.Variable(self.html5_required),
            )

        field, attrs, html5_required = context.render_context[self]
        field = field.resolve(context)
        try:
            html5_required = html5_required.resolve(context)
        except template.VariableDoesNotExist:
            html5_required = False

        # Pick up the template pack if it has been overridden in FormHelper
        template_pack = context.get("template_pack", TEMPLATE_PACK)

        # There are special django widgets that wrap actual widgets,
        # such as forms.widgets.MultiWidget, admin.widgets.RelatedFieldWidgetWrapper
        widgets = getattr(
            field.field.widget,
            "widgets",
            [getattr(field.field.widget, "widget", field.field.widget)],
        )

        if template_pack == "tbx":
            if is_multivalue(field):
                error_widgets = [field.widget for field in field.field.fields]
                error_count = sum(
                    len(getattr(widget, "errors", []))
                    for widget in error_widgets
                )
            else:
                error_widgets = None
                error_count = 0

        if isinstance(attrs, dict):
            attrs = [attrs] * len(widgets)

        converters = {
            "checkboxinput": "tbxforms-checkboxes__input",
            "select": "tbxforms-select",
            "lazyselect": "tbxforms-select",
            "textarea": "tbxforms-textarea",
            "clearablefileinput": "tbxforms-file-upload",
            "textinput": "tbxforms-input tbxforms-input--text",
            "urlinput": "tbxforms-input tbxforms-input--url",
            "numberinput": "tbxforms-input tbxforms-input--number",
            "emailinput": "tbxforms-input tbxforms-input--email",
            "passwordinput": "tbxforms-input tbxforms-input--password",
        }
        converters.update(getattr(settings, "CRISPY_CLASS_CONVERTERS", {}))

        for widget_idx, (widget, attr) in enumerate(zip(widgets, attrs)):
            class_name = widget.__class__.__name__.lower()
            class_name = converters.get(class_name, class_name)

            if class_name:
                css_class = class_name.split()
            else:
                css_class = []

            for attr_css_class in widget.attrs.get("class", "").split():
                if attr_css_class not in css_class:
                    css_class.append(attr_css_class)

            css_class = " ".join(css_class)

            if template_pack == "tbx":
                # The ability to override input_type was added to avoid having to
                # create new widgets. However, as a result, the browser validates
                # the field and displays a red border with no feedback to the user.
                # That is at odds with with the way the Design System reports errors.
                # However this is being left in for now until the "conflict" is better
                # understood - it might be useful to somebody at some point.

                if (
                    hasattr(widget, "input_type")
                    and "input_type" in widget.attrs
                ):
                    widget.input_type = widget.attrs.pop("input_type")

                if field.help_text and not is_multivalue(field):
                    widget.attrs["aria-describedby"] = (
                        "%s_hint" % field.auto_id
                    )

                if (
                    "class" in widget.attrs
                    and "tbxforms-js-character-count" in widget.attrs["class"]
                ):

                    # The javascript that updates the span containing character count
                    # as the user types expects the id to end in '-info'. Anything else
                    # won't work.

                    if widget.attrs["aria-describedby"]:
                        widget.attrs["aria-describedby"] += (
                            " %s-info" % field.auto_id
                        )
                    else:
                        widget.attrs["aria-describedby"] = (
                            "%s-info" % field.auto_id
                        )

                if field.errors:
                    widget_class_name = widget.__class__.__name__

                    if widget_class_name in [
                        "Select",
                        "TextInput",
                        "Textarea",
                    ]:
                        if is_multivalue(field):
                            if error_count == 0:
                                css_class += " tbxforms-input--error"
                            elif getattr(
                                error_widgets[widget_idx], "errors", None
                            ):
                                css_class += " tbxforms-input--error"
                        else:
                            css_class += " tbxforms-input--error"
                    elif widget_class_name in [
                        "FileInput",
                        "ClearableFileInput",
                    ]:
                        css_class += " tbxforms-file-upload--error"

                    if not field.help_text:
                        widget.attrs["aria-describedby"] = ""

                    for error_idx, error in enumerate(field.errors, start=1):
                        css_error_class = "%s_%d_error" % (
                            field.auto_id,
                            error_idx,
                        )

                        if is_multivalue(field):
                            if getattr(
                                error_widgets[widget_idx], "errors", None
                            ):
                                if error in error_widgets[widget_idx].errors:
                                    if "aria-describedby" not in widget.attrs:
                                        widget.attrs["aria-describedby"] = ""

                                    if widget.attrs["aria-describedby"]:
                                        widget.attrs["aria-describedby"] += " "

                                    widget.attrs[
                                        "aria-describedby"
                                    ] += css_error_class
                        else:
                            if "aria-describedby" not in widget.attrs:
                                widget.attrs["aria-describedby"] = ""

                            if widget.attrs["aria-describedby"]:
                                widget.attrs["aria-describedby"] += " "

                            widget.attrs["aria-describedby"] += css_error_class

            widget.attrs["class"] = css_class

            # Convert conditional dict to two separate JS-friendly variables.
            if "data-conditional" in widget.attrs:
                conditional_attrs = ast.literal_eval(
                    html.unescape(widget.attrs.pop("data-conditional"))
                )
                widget.attrs[
                    "data-conditional-field-name"
                ] = conditional_attrs["field_name"]
                widget.attrs["data-conditional-field-values"] = json.dumps(
                    conditional_attrs["values"]
                )

            # HTML5 required attribute
            if (
                html5_required
                and field.field.required
                and "required" not in widget.attrs
            ):
                if field.field.widget.__class__.__name__ != "RadioSelect":
                    widget.attrs["required"] = "required"

            for attribute_name, attribute in attr.items():
                attribute_name = template.Variable(attribute_name).resolve(
                    context
                )

                if attribute_name in widget.attrs:
                    widget.attrs[attribute_name] += " " + template.Variable(
                        attribute
                    ).resolve(context)
                else:
                    widget.attrs[attribute_name] = template.Variable(
                        attribute
                    ).resolve(context)

        return str(field)


@register.tag(name="crispy_tbx_field")
def crispy_tbx_field(parser, token):
    """
    The template tag used to render fields from the template pack.

    Examples: ::

        {% crispy_tbx_field field attrs %}

    The code was copied over verbatim from ``django-crispy-forms``. Any additions
    are clearly marked with a check to see if the 'gds' template pack is being
    used.

    This template tag is only used within the tbx/field.html template and you
    almost certainly will not have to deal with it, even if you are laying out a
    form explicitly.

    """
    token = token.split_contents()
    field = token.pop(1)
    attrs = {}

    # We need to pop tag name, or pairwise would fail
    token.pop(0)
    for attribute_name, value in pairwise(token):
        attrs[attribute_name] = value

    return CrispyGDSFieldNode(field, attrs)
