"""
Tests to verify date inputs are rendered correctly.
"""

import datetime

from tests.forms import DateInputForm
from tests.utils import render_form

# IMPORTANT: The test results are totally dependent on the require_all_fields
# attribute on the DateInputField. Test tests here use
# require_all_fields = False so there is a clear separation between field
# level errors and errors from the day, month and year fields.


def test_initial_attributes(snapshot_html):
    """Verify all the gds attributes are displayed."""
    form = DateInputForm(
        initial={"date": datetime.date(year=2007, month=11, day=12)}
    )
    assert render_form(form) == snapshot_html


def test_field_error_attributes(snapshot_html):
    """
    Verify the parent field level error messages are displayed correctly.
    """
    form = DateInputForm(data={"date_0": "", "date_1": "", "date_2": ""})
    assert not form.is_valid()
    assert render_form(form) == snapshot_html


def test_subfield_error_attributes(snapshot_html):
    """
    Verify the error messages for the individual fields are displayed
    correctly.
    """
    form = DateInputForm(data={"date_0": "a", "date_1": "11", "date_2": ""})
    assert not form.is_valid()
    assert render_form(form) == snapshot_html


def test_non_required_field_left_blank_does_not_raise_exception(snapshot_html):
    """Verify all the gds attributes are displayed."""
    form = DateInputForm(data={"date_0": "", "date_1": "", "date_2": ""})
    form.fields["date"].required = False
    assert form.is_valid()
    assert render_form(form) == snapshot_html


def test_optional_field_highlighting(snapshot_html):
    """
    Ensure optional fields are marked with "(optional)" by default.
    """
    form = DateInputForm()
    form.fields["date"].required = False
    assert render_form(form) == snapshot_html


def test_required_field_highlighting(highlight_required_fields, snapshot_html):
    """
    Ensure fields can be marked with "*" instead of "(optional)".
    """
    form = DateInputForm()
    assert render_form(form) == snapshot_html
