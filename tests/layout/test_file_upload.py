"""
Tests to verify file uploads are rendered correctly.

"""
from tbxforms.layout import (
    Field,
    Layout,
    Size,
)
from tests.forms import FileUploadForm
from tests.utils import render_form


def test_initial_attributes(snapshot_html):
    """Verify all the gds attributes are displayed."""
    form = FileUploadForm()
    assert render_form(form) == snapshot_html


def test_validation_error_attributes(snapshot_html):
    """Verify all the gds error attributes are displayed."""
    form = FileUploadForm(data={})
    assert not form.is_valid()
    assert render_form(form) == snapshot_html


def test_show_label_as_heading(snapshot_html):
    """Verify the field label can be displayed as the page heading."""
    form = FileUploadForm()
    form.helper.layout = Layout(Field("file", context={"label_tag": "h1"}))
    assert render_form(form) == snapshot_html


def test_change_label_size(snapshot_html):
    """Verify size of the field label can be changed from the default."""
    form = FileUploadForm()
    form.helper.layout = Layout(
        Field("file", context={"label_size": Size.for_label("l")})
    )
    assert render_form(form) == snapshot_html


def test_no_label(snapshot_html):
    """Verify field is rendered correctly if no label is given."""
    form = FileUploadForm()
    form.fields["file"].label = ""
    assert render_form(form) == snapshot_html


def test_no_help_text(snapshot_html):
    """Verify field is rendered correctly if no help text is given."""
    form = FileUploadForm()
    form.fields["file"].help_text = ""
    assert render_form(form) == snapshot_html


def test_no_help_text_errors(snapshot_html):
    """
    Verify all the gds error attributes are displayed if no help text is given.
    """
    form = FileUploadForm(data={})
    form.fields["file"].help_text = ""
    assert render_form(form) == snapshot_html
