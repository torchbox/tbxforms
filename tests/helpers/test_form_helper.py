"""
Tests to verify text fields are rendered correctly.
"""

from tbxforms.layout import (
    Field,
    Layout,
    Size,
)
from tests.forms import (
    CheckboxesForm,
    CheckboxForm,
    TextInputForm,
)
from tests.utils import render_form


def test_default_label_size(snapshot_html):
    """Verify a default label size can set for fields."""
    form = TextInputForm()
    form.helper.label_size = Size.SMALL
    assert render_form(form) == snapshot_html


def test_override_default_label_size(snapshot_html):
    """Verify a default label size can be overridden on the field."""
    form = TextInputForm()
    form.helper.label_size = Size.SMALL
    form.helper.layout = Layout(Field.text("name", label_size=Size.LARGE))
    assert render_form(form) == snapshot_html


def test_default_legend_size(snapshot_html):
    """Verify a default legend size can set for fields."""
    form = CheckboxesForm()
    form.helper.legend_size = Size.SMALL
    assert render_form(form) == snapshot_html


def test_override_default_legend_size(snapshot_html):
    """Verify a default legend size can be overridden on the field."""
    form = CheckboxesForm()
    form.helper.legend_size = Size.SMALL
    form.helper.layout = Layout(
        Field.checkboxes("method", legend_size=Size.LARGE)
    )
    assert render_form(form) == snapshot_html


def test_error_summary_shown_by_default(snapshot_html):
    """Verify the error summary is shown by default."""
    form = CheckboxForm(data={"accept": True})
    form.add_error(None, "An example non-field error.")
    assert not form.is_valid()

    rendered_form = render_form(form)
    assert rendered_form == snapshot_html
    assert "There is a problem with your submission" in rendered_form


def test_error_summary_can_be_hidden(snapshot_html):
    """Verify the error summary can be hidden."""
    form = CheckboxForm(data={"accept": True})
    form.add_error(None, "An example non-field error.")
    form.helper.show_error_summary = False
    assert not form.is_valid()

    rendered_form = render_form(form)
    assert rendered_form == snapshot_html
    assert "There is a problem with your submission" not in rendered_form
