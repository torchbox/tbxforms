"""
Tests to verify text fields are rendered correctly.
"""

from tbxforms.layout import (
    Field,
    Layout,
    Size,
)
from tests.forms import TextInputForm
from tests.utils import render_form


def test_initial_attributes(snapshot_html):
    """Verify all the gds attributes are displayed."""
    form = TextInputForm(initial={"name": "Field value"})
    assert render_form(form) == snapshot_html


def test_validation_error_attributes(snapshot_html):
    """Verify all the gds error attributes are displayed."""
    form = TextInputForm(data={"name": ""})
    assert not form.is_valid()
    assert render_form(form) == snapshot_html


def test_show_label_as_heading(snapshot_html):
    """Verify the field label can be displayed as the page heading."""
    form = TextInputForm()
    form.helper.layout = Layout(Field.text("name", label_tag="h1"))
    assert render_form(form) == snapshot_html


def test_change_label_size(snapshot_html):
    """Verify size of the field label can be changed from the default."""
    form = TextInputForm()
    form.helper.layout = Layout(Field.text("name", label_size=Size.LARGE))
    assert render_form(form) == snapshot_html


def test_no_label(snapshot_html):
    """Verify field is rendered correctly if no label is given."""
    form = TextInputForm()
    form.fields["name"].label = ""
    assert render_form(form) == snapshot_html


def test_no_help_text(snapshot_html):
    """Verify field is rendered correctly if no help text is given."""
    form = TextInputForm()
    form.fields["name"].help_text = ""
    assert render_form(form) == snapshot_html


def test_no_help_text_errors(snapshot_html):
    """
    Verify all the gds error attributes are displayed if no help text is given.
    """
    form = TextInputForm(data={"name": ""})
    form.fields["name"].help_text = ""
    assert not form.is_valid()
    assert render_form(form) == snapshot_html
