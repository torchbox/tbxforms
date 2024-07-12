"""
Tests to verify textareas are rendered correctly.
"""

from django.test import override_settings

import pytest

from tbxforms.layout import (
    Field,
    Layout,
    Size,
)
from tests.forms import TextareaForm
from tests.utils import render_form


def test_initial_attributes(snapshot_html):
    """Verify all the gds attributes are displayed."""
    form = TextareaForm(initial={"description": "Field value"})
    assert render_form(form) == snapshot_html


def test_validation_error_attributes(snapshot_html):
    """Verify all the gds error attributes are displayed."""
    form = TextareaForm(data={"description": ""})
    assert not form.is_valid()
    assert render_form(form) == snapshot_html


def test_show_label_as_heading(snapshot_html):
    """Verify the field label can be displayed as the page heading."""
    form = TextareaForm()
    form.helper.layout = Layout(Field.textarea("description", label_tag="h1"))
    assert render_form(form) == snapshot_html


def test_change_label_size(snapshot_html):
    """Verify size of the field label can be changed from the default."""
    form = TextareaForm()
    form.helper.layout = Layout(
        Field.textarea("description", label_size=Size.LARGE)
    )
    assert render_form(form) == snapshot_html


def test_no_label(snapshot_html):
    """Verify field is rendered correctly if no label is given."""
    form = TextareaForm()
    form.fields["description"].label = ""
    assert render_form(form) == snapshot_html


def test_no_help_text(snapshot_html):
    """Verify field is rendered correctly if no help text is given."""
    form = TextareaForm()
    form.fields["description"].help_text = ""
    assert render_form(form) == snapshot_html


def test_no_help_text_errors(snapshot_html):
    """
    Verify all the gds error attributes are displayed if no help text is given.
    """
    form = TextareaForm(data={"description": ""})
    form.fields["description"].help_text = ""
    assert render_form(form) == snapshot_html


def test_character_count(snapshot_html):
    """Verify the field can show the maximum number of characters allowed."""
    form = TextareaForm(initial={"description": "Field value"})
    form.helper.layout = Layout(
        Field.textarea("description", max_characters=100)
    )
    assert render_form(form) == snapshot_html


def test_character_and_word_count(snapshot_html):
    """
    Verify an exception is raise if the character and words count is given.
    """
    with pytest.raises(ValueError):
        Field.textarea("description", max_characters=100, max_words=50)


def test_threshold(snapshot_html):
    """
    Verify info is shown after a certain number of words has been entered.
    """
    form = TextareaForm(initial={"description": "Field value"})
    form.helper.layout = Layout(
        Field.textarea("description", max_words=100, threshold=50)
    )
    assert render_form(form) == snapshot_html


def test_character_threshold():
    """Verify an exception is raise if the threshold is set with no limit."""
    with pytest.raises(ValueError):
        Field.textarea("description", threshold=50)


def test_optional_field_highlighting(snapshot_html):
    """
    Ensure optional fields are marked with "(optional)" by default.
    """
    form = TextareaForm()
    form.fields["description"].required = False
    assert render_form(form) == snapshot_html


@override_settings(TBXFORMS_HIGHLIGHT_REQUIRED_FIELDS=True)
def test_required_field_highlighting(snapshot_html):
    """
    Ensure fields can be marked with "*" instead of "(optional)".
    """
    form = TextareaForm()
    assert render_form(form) == snapshot_html
