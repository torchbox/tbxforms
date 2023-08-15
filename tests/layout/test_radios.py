"""
Tests to verify radio buttons are rendered correctly.

"""
from tbxforms.layout import (
    Field,
    Layout,
    Size,
)
from tests.forms import (
    RadiosChoiceForm,
    RadiosForm,
)
from tests.utils import render_form


def test_initial_attributes(snapshot_html):
    """Verify all the gds attributes are displayed."""
    form = RadiosForm(initial={"method": "email"})
    assert render_form(form) == snapshot_html


def test_validation_error_attributes(snapshot_html):
    """Verify all the gds error attributes are displayed."""
    form = RadiosForm(data={"method": ""})
    assert not form.is_valid()
    assert render_form(form) == snapshot_html


def test_choices(snapshot_html):
    """Verify hints and dividers are displayed."""
    form = RadiosChoiceForm(initial={"method": "email"})
    assert render_form(form) == snapshot_html


def test_small(snapshot_html):
    """Verify size of the radio buttons can be changed."""
    form = RadiosForm()
    form.helper.layout = Layout(Field.radios("method", small=True))
    assert render_form(form) == snapshot_html


def test_inline(snapshot_html):
    """Verify radio buttons can be displayed in a row."""
    form = RadiosForm()
    form.helper.layout = Layout(Field.radios("method", inline=True))
    assert render_form(form) == snapshot_html


def test_show_legend_as_heading(snapshot_html):
    """Verify the field legend can be displayed as the page heading."""
    form = RadiosForm()
    form.helper.layout = Layout(Field.radios("method", legend_tag="h1"))
    assert render_form(form) == snapshot_html


def test_change_legend_size(snapshot_html):
    """Verify size of the field legend can be changed from the default."""
    form = RadiosForm()
    form.helper.layout = Layout(Field.radios("method", legend_size=Size.LARGE))
    assert render_form(form) == snapshot_html


def test_no_legend(snapshot_html):
    """Verify field is rendered correctly if no label is given."""
    form = RadiosForm()
    form.fields["method"].label = ""
    assert render_form(form) == snapshot_html


def test_no_help_text(snapshot_html):
    """Verify field is rendered correctly if no help text is given."""
    form = RadiosForm()
    form.fields["method"].help_text = ""
    assert render_form(form) == snapshot_html


def test_no_help_text_errors(snapshot_html):
    """
    Verify all the gds error attributes are displayed if no help text is given.
    """
    form = RadiosForm(data={"method": ""})
    form.fields["method"].help_text = ""
    assert render_form(form) == snapshot_html
