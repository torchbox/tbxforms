"""
Tests to verify text fields are rendered correctly.

"""
from tbxforms.helper import FormHelper
from tbxforms.layout import (
    Field,
    Layout,
    Size,
)
from tests.forms import (
    CheckboxesForm,
    TextInputForm,
)
from tests.utils import render_form


def test_default_label_size(snapshot_html):
    """Verify a default label size can set for fields."""
    form = TextInputForm()
    form.helper = FormHelper(form)
    form.helper.label_size = Size.MEDIUM
    assert render_form(form) == snapshot_html


def test_override_default_label_size(snapshot_html):
    """Verify a default label size can be overridden on the field."""
    form = TextInputForm()
    form.helper = FormHelper()
    form.helper.label_size = Size.MEDIUM
    form.helper.layout = Layout(Field.text("name", label_size=Size.LARGE))
    assert render_form(form) == snapshot_html


def test_default_legend_size(snapshot_html):
    """Verify a default legend size can set for fields."""
    form = CheckboxesForm()
    form.helper = FormHelper(form)
    form.helper.legend_size = Size.MEDIUM
    assert render_form(form) == snapshot_html


def test_override_default_legend_size(snapshot_html):
    """Verify a default legend size can be overridden on the field."""
    form = CheckboxesForm()
    form.helper = FormHelper()
    form.helper.legend_size = Size.MEDIUM
    form.helper.layout = Layout(
        Field.checkboxes("method", legend_size=Size.LARGE)
    )
    assert render_form(form) == snapshot_html
