"""
Tests to verify selects are rendered correctly.
"""

from django.test import override_settings

from tbxforms.layout import (
    Field,
    Layout,
    Size,
)
from tests.forms import SelectForm
from tests.utils import render_form


def test_initial_attributes(snapshot_html):
    """Verify all the gds attributes are displayed."""
    form = SelectForm(initial={"method": "email"})
    assert render_form(form) == snapshot_html


def test_validation_error_attributes(snapshot_html):
    """Verify all the gds error attributes are displayed."""
    form = SelectForm(data={"method": ""})
    assert not form.is_valid()
    assert render_form(form) == snapshot_html


def test_show_label_as_heading(snapshot_html):
    """Verify the field label can be displayed as the page heading."""
    form = SelectForm()
    form.helper.layout = Layout(Field.select("method", label_tag="h1"))
    assert render_form(form) == snapshot_html


def test_change_label_size(snapshot_html):
    """Verify size of the field label can be changed from the default."""
    form = SelectForm()
    form.helper.layout = Layout(Field.select("method", label_size=Size.LARGE))
    assert render_form(form) == snapshot_html


def test_no_label(snapshot_html):
    """Verify field is rendered correctly if no label is given."""
    form = SelectForm()
    form.fields["method"].label = ""
    assert render_form(form) == snapshot_html


def test_no_help_text(snapshot_html):
    """Verify field is rendered correctly if no help text is given."""
    form = SelectForm()
    form.fields["method"].help_text = ""
    assert render_form(form) == snapshot_html


def test_no_help_text_errors(snapshot_html):
    """
    Verify all the gds error attributes are displayed if no help text is given.
    """
    form = SelectForm(data={"method": ""})
    form.fields["method"].help_text = ""
    assert render_form(form) == snapshot_html


def test_optional_field_highlighting(snapshot_html):
    """
    Ensure optional fields are marked with "(optional)" by default.
    """
    form = SelectForm()
    form.fields["method"].required = False
    assert render_form(form) == snapshot_html


@override_settings(TBXFORMS_HIGHLIGHT_REQUIRED_FIELDS=True)
def test_required_field_highlighting(snapshot_html):
    """
    Ensure fields can be marked with "*" instead of "(optional)".
    """
    form = SelectForm()
    assert render_form(form) == snapshot_html
