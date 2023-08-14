"""
Tests to verify a single (boolean) checkbox is rendered correctly.

"""
from tbxforms.layout import (
    Field,
    Layout,
)
from tests.forms import CheckboxForm
from tests.utils import render_form


def test_initial_attributes(snapshot_html):
    """Verify all the gds attributes are displayed."""
    form = CheckboxForm(initial={"accept": True})
    assert render_form(form) == snapshot_html


def test_validation_error_attributes(snapshot_html):
    """Verify all the gds error attributes are displayed."""
    form = CheckboxForm(data={"accept": ""})
    assert not form.is_valid()
    assert render_form(form) == snapshot_html


def test_checkbox_size(snapshot_html):
    """Verify size of the checkbox can be changed from the default."""
    form = CheckboxForm()
    form.helper.layout = Layout(
        Field("accept", context={"checkboxes_small": True})
    )
    assert render_form(form) == snapshot_html


def test_no_help_text(snapshot_html):
    """Verify field is rendered correctly if no help text is given."""
    form = CheckboxForm()
    form.fields["accept"].help_text = ""
    assert render_form(form) == snapshot_html


def test_no_help_text_errors(snapshot_html):
    """
    Verify all the gds error attributes are displayed if no help text is given.
    """
    form = CheckboxForm(data={"accept": ""})
    form.fields["accept"].help_text = ""
    assert render_form(form) == snapshot_html
