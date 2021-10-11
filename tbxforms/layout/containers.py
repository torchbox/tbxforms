import json

from django.template.loader import render_to_string

from crispy_forms import layout as crispy_forms_layout
from crispy_forms.utils import (
    TEMPLATE_PACK,
    flatatt,
)

from tbxforms.layout import Size


class Div(crispy_forms_layout.Div):
    """
    A layout object for displaying a general-purpose Div. This is not
    a Design System component but is included as it's a basic part of
    ``django-crispy-forms``.

    Although there is the Fieldset component for grouping fields together
    a Div is quite useful when you just need to add some spacing between
    elements.

    Examples::

        Div("name", "email", "phone", css_class="tbxforms-!-margin-bottom-5")
        Div("street", "city", "post_code")

    Arguments:
        css_id (str, optional): an unique identifier for the <div>. Generally
            you will need to set this if you need to add some javascript or
            very specific styling.

        css_class (str, optional): the names of one or more CSS classes that
            will be added to the <div>. This parameter is for any styling you
            want to apply. Nothing is added by default.

        template (str, optional): the path to a template that overrides the
            one normally used.

        *fields: a list of layout objects - fields, buttons, HTML,
            etc. that displayed inside the <div> element.

        **kwargs: any additional attributes you want to add to the parent
            <div>.

    """

    def __init__(self, *fields, **kwargs):
        if "data_conditional" in kwargs:
            conditional_attrs = kwargs.pop("data_conditional")
            kwargs["data_conditional_field_name"] = conditional_attrs[
                "field_name"
            ]
            kwargs["data_conditional_field_values"] = json.dumps(
                conditional_attrs["values"]
            )
        super().__init__(*fields, **kwargs)


class Fieldset(crispy_forms_layout.LayoutObject):
    """
    A layout object for displaying groups of fields.

    The contents of a Fieldset are be one or more LayoutObjects: fields,
    buttons, composed layouts, etc. You can give the <fieldset> a <legend>
    title, set the size of the font used and wrap the <legend> in a heading
    tag if necessary.

    Examples::

        Fieldset('form_field_1', 'form_field_2')
        Fieldset('form_field_1', 'form_field_2', legend="title")
        Fieldset(
            'form_field_1', 'form_field_2', legend="title", legend_tag="h1"
        )
        Fieldset(
            'form_field_1', 'form_field_2', legend="title", legend_size="xl"
        )

    Arguments:
        legend (str, optional): the title displayed in a <legend>.

        legend_size (str, optional): the size of the title: 's', 'm', 'l' or
            'xl'. It's more readable if you use the contants on the ``Size``
            class.

        legend_tag (str, optional): an HTML tag that wraps the <legend>.
            Typically this is 'h1' so the <legend> also acts as the page title.

        css_id (str, optional): an unique identifier for the fieldset.

        css_class (str, optional): the names of one or more CSS classes that
            will be added to the <fieldset>. The basic Design System CSS
            classes will be added automatically. This parameter is for any
            extra styling you want to apply.

        template (str, optional): the path to a template that overrides the
            one provided by the template pack.

        *fields: a list of LayoutObjects objects that make up the Fieldset
            contents.

        **kwargs:  any additional attributes you want to add to the <fieldset>.

    """

    css_class = "tbxforms-fieldset"
    template = "%s/layout/fieldset.html"

    def __init__(
        self, *fields, legend=None, legend_size=None, legend_tag=None, **kwargs
    ):
        self.fields = list(fields)
        self.context = {}

        if legend:
            self.context["legend"] = legend

        if legend_size:
            self.context["legend_size"] = Size.for_legend(legend_size)

        if legend_tag:
            self.context["legend_tag"] = legend_tag

        if hasattr(self, "css_class") and "css_class" in kwargs:
            self.css_class += " %s" % kwargs.pop("css_class")
        if not hasattr(self, "css_class"):
            self.css_class = kwargs.pop("css_class", None)

        if "data_conditional" in kwargs:
            conditional_attrs = kwargs.pop("data_conditional")
            kwargs["data_conditional_field_name"] = conditional_attrs[
                "field_name"
            ]
            kwargs["data_conditional_field_values"] = json.dumps(
                conditional_attrs["values"]
            )

        self.css_id = kwargs.pop("css_id", None)
        self.template = kwargs.pop("template", self.template)
        self.flat_attrs = flatatt(kwargs)

    def render(
        self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs
    ):
        fields = self.get_rendered_fields(
            form, form_style, context, template_pack, **kwargs
        )
        context = {
            "fieldset": self,
            "fields": fields,
            "form_style": form_style,
        }
        context.update(self.context)
        template = self.get_template_name(template_pack)
        return render_to_string(template, context)
