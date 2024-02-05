"""
Tests to verify fieldsets are rendered correctly.
"""

from tbxforms.layout import (
    Fieldset,
    Layout,
    Size,
)
from tests.forms import FieldsetForm
from tests.utils import render_form


def test_basic_layout(snapshot_html):
    """Verify all the gds attributes are displayed."""
    form = FieldsetForm()
    assert render_form(form) == snapshot_html


def test_show_legend_as_heading(snapshot_html):
    """Verify the field legend can be displayed as the page heading."""
    form = FieldsetForm()
    form.helper.layout = Layout(
        Fieldset(
            "name",
            "email",
            legend="Contact",
            legend_tag="h1",
        )
    )
    rendered_form = render_form(form)
    assert rendered_form == snapshot_html
    assert "<h1" in rendered_form


def test_change_legend_size(snapshot_html):
    """Verify size of the field legend can be changed from the default."""
    form = FieldsetForm()
    form.helper.layout = Layout(
        Fieldset(
            "name",
            "email",
            legend="Contact",
            legend_size=Size.LARGE,
        )
    )
    rendered_form = render_form(form)
    assert rendered_form == snapshot_html
    assert "tbxforms-fieldset__legend--l" in rendered_form


def test_css_class(snapshot_html):
    """Verify an extra CSS class can be added to the fieldset."""
    form = FieldsetForm()
    form.helper.layout = Layout(
        Fieldset(
            "name",
            "email",
            legend="Contact",
            css_class="extra-css-class",
        )
    )
    rendered_form = render_form(form)
    assert rendered_form == snapshot_html
    assert (
        'class="tbxforms-form-group tbxforms-fieldset extra-css-class"'
        in rendered_form
    )


def test_css_id(snapshot_html):
    """Verify the id attribute can be set on the fieldset."""
    form = FieldsetForm()
    form.helper.layout = Layout(
        Fieldset(
            "name",
            "email",
            legend="Contact",
            css_id="new_id",
        ),
    )
    rendered_form = render_form(form)
    assert rendered_form == snapshot_html
    assert 'id="div_id_name"' in rendered_form


def test_attribute(snapshot_html):
    """Verify the extra attributes can be added."""
    form = FieldsetForm()
    form.helper.layout = Layout(
        Fieldset(
            "name",
            "email",
            legend="Contact",
            key="value",
        )
    )
    rendered_form = render_form(form)
    assert rendered_form == snapshot_html
    assert 'key="value"' in rendered_form
