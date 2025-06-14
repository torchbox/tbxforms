"""
Tests to verify checkboxes are rendered correctly.
"""

from django.test import override_settings

from tbxforms.layout import (
    Field,
    Layout,
    Size,
)
from tests.forms import (
    CheckboxesChoiceForm,
    CheckboxesForm,
)
from tests.utils import render_form


def test_initial_attributes(snapshot_html):
    """Verify all the gds attributes are displayed."""
    form = CheckboxesForm(initial={"method": ["email", "text"]})
    assert render_form(form) == snapshot_html


def test_validation_error_attributes(snapshot_html):
    """Verify all the gds error attributes are displayed."""
    form = CheckboxesForm(data={"method": ""})
    assert not form.is_valid()
    assert render_form(form) == snapshot_html


def test_choices(snapshot_html):
    """Verify that hints are displayed."""
    form = CheckboxesChoiceForm(initial={"method": ["email", "text"]})
    assert render_form(form) == snapshot_html


def test_checkbox_size(snapshot_html):
    """Verify size of the checkbox can be changed from the default."""
    form = CheckboxesForm()
    form.helper.layout = Layout(Field.checkboxes("method", small=True))
    assert render_form(form) == snapshot_html


def test_show_legend_as_heading(snapshot_html):
    """Verify the field legend can be displayed as the page heading."""
    form = CheckboxesForm()
    form.helper.layout = Layout(Field.checkboxes("method", legend_tag="h1"))
    assert render_form(form) == snapshot_html


def test_change_legend_size(snapshot_html):
    """Verify size of the field legend can be changed from the default."""
    form = CheckboxesForm()
    form.helper.layout = Layout(
        Field.checkboxes("method", legend_size=Size.LARGE)
    )
    assert render_form(form) == snapshot_html


def test_no_legend(snapshot_html):
    """Verify field is rendered correctly if no label is given."""
    form = CheckboxesForm()
    form.fields["method"].label = ""
    assert render_form(form) == snapshot_html


def test_no_help_text(snapshot_html):
    """Verify field is rendered correctly if no help text is given."""
    form = CheckboxesForm()
    form.fields["method"].help_text = ""
    assert render_form(form) == snapshot_html


def test_no_help_text_errors(snapshot_html):
    """
    Verify all the gds error attributes are displayed if no help text is given.
    """
    form = CheckboxesForm(data={"method": ""})
    form.fields["method"].help_text = ""
    assert render_form(form) == snapshot_html


def test_optional_field_highlighting(snapshot_html):
    """
    Ensure optional fields are marked with "(optional)" by default.
    """
    form = CheckboxesForm()
    form.fields["method"].required = False
    assert render_form(form) == snapshot_html


@override_settings(TBXFORMS_HIGHLIGHT_REQUIRED_FIELDS=True)
def test_required_field_highlighting(snapshot_html):
    """
    Ensure fields can be marked with "*" instead of "(optional)".
    """
    form = CheckboxesForm()
    assert render_form(form) == snapshot_html


@override_settings(TBXFORMS_HIGHLIGHT_REQUIRED_FIELDS=True)
def test_required_field_highlighting_disabled_per_form(snapshot_html):
    """
    Ensure that required field highlighting can be turned off per-form.
    """
    form = CheckboxesForm()
    form.helper.highlight_required_fields = False
    form.fields["method"].required = False
    assert render_form(form) == snapshot_html


@override_settings(TBXFORMS_HIGHLIGHT_REQUIRED_FIELDS=False)
def test_required_field_highlighting_enabled_per_form(snapshot_html):
    form = CheckboxesForm()
    form.helper.highlight_required_fields = True
    assert render_form(form) == snapshot_html
