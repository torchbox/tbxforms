"""
Tests to verify the DateInputField.
"""

import datetime

from django.core.exceptions import ValidationError

import pytest

from tbxforms.fields import DateInputField


def test_compress_invalid_fields():
    """Verify compress raises an error on an invalid date."""
    day = 30
    month = 2
    year = 2021
    field = DateInputField()
    with pytest.raises(ValidationError, match="day is out of range for month"):
        field.compress([day, month, year])


def test_compress_valid_fields():
    """Verify compress returns a date."""
    date = datetime.date(year=2007, month=12, day=11)
    field = DateInputField()
    value = field.compress([date.day, date.month, date.year])
    assert value == date


def test_compress_optional_fields_empty():
    """
    Verify compress returns None if the values are not required and not set.
    """
    field = DateInputField()
    field.require_all_fields = False
    value = field.compress(["", "", ""])
    assert value is None


def test_cleaned_valid_value():
    """Verify the Date input field returns a date object."""
    date = datetime.date(year=2007, month=12, day=11)
    field = DateInputField()
    value = field.clean([date.day, date.month, date.year])
    assert value == date


def test_required_day_field():
    """
    Verify a parent field required error is not recorded on the day widget.
    """
    field = DateInputField()
    with pytest.raises(ValidationError) as err:
        field.clean(["", "12", "2007"])
    assert field.fields[0].widget.errors == []
    assert err.value.args[0] == field.error_messages["required"]


def test_incomplete_day_field():
    """Verify an incomplete error on the day field is saved in the widget."""
    field = DateInputField(require_all_fields=False)
    with pytest.raises(ValidationError) as err:
        field.clean(["", "12", "2007"])
    assert err.value.args[0][0] in field.fields[0].widget.errors
    assert err.value.args[0][0] == field.fields[0].error_messages["incomplete"]


def test_invalid_day_field():
    """Verify a validation error on the day field is saved in the widget."""
    field = DateInputField()
    with pytest.raises(ValidationError) as err:
        field.clean(["a", "12", "2007"])
    error = err.value.args[0][0].args[0]
    assert error in field.fields[0].widget.errors
    assert error == field.fields[0].validators[0].message


def test_required_month_field():
    """
    Verify a parent field required error is not recorded on the month widget.
    """
    field = DateInputField()
    with pytest.raises(ValidationError) as err:
        field.clean(["11", "", "2007"])
    assert field.fields[1].widget.errors == []
    assert err.value.args[0] == field.error_messages["required"]


def test_incomplete_month_field():
    """Verify an incomplete error on the month field is saved in the widget."""
    field = DateInputField(require_all_fields=False)
    with pytest.raises(ValidationError) as err:
        field.clean(["11", "", "2007"])
    assert err.value.args[0][0] in field.fields[1].widget.errors
    assert err.value.args[0][0] == field.fields[1].error_messages["incomplete"]


def test_invalid_month_field():
    """Verify a validation error on the month field is saved in the widget."""
    field = DateInputField()
    with pytest.raises(ValidationError) as err:
        field.clean(["11", "a", "2007"])
    error = err.value.args[0][0].args[0]
    assert error in field.fields[1].widget.errors
    assert error == field.fields[1].validators[0].message


def test_required_year_field():
    """
    Verify a parent field required error is not recorded on the year widget.
    """
    field = DateInputField()
    with pytest.raises(ValidationError) as err:
        field.clean(["11", "12", ""])
    assert field.fields[1].widget.errors == []
    assert err.value.args[0] == field.error_messages["required"]


def test_incomplete_year_field():
    """Verify an incomplete error on the month field is saved in the widget."""
    field = DateInputField(require_all_fields=False)
    with pytest.raises(ValidationError) as err:
        field.clean(["11", "12", ""])
    assert err.value.args[0][0] in field.fields[2].widget.errors
    assert err.value.args[0][0] == field.fields[2].error_messages["incomplete"]


def test_invalid_year_field():
    """Verify a validation error on the month field is saved in the widget."""
    field = DateInputField()
    with pytest.raises(ValidationError) as err:
        field.clean(["11", "12", "a"])
    error = err.value.args[0][0].args[0]
    assert error in field.fields[2].widget.errors
    assert error == field.fields[2].validators[0].message


def test_out_of_range_day_field():
    """Verify an out of range day is not allowed."""
    field = DateInputField()
    with pytest.raises(ValidationError) as err:
        field.clean(["32", "2", "2006"])
    error = err.value.args[0][0]
    assert error == (
        "'32' is not a valid day for February 2006 - "
        "please enter a value between 1 and 28."
    )


def test_zero_value_day_field():
    """Verify a zero day is not allowed."""
    field = DateInputField()
    with pytest.raises(ValidationError) as err:
        field.clean(["0", "2", "2006"])
    error = err.value.args[0][0].args[0]
    assert error in field.fields[0].widget.errors
    assert error == field.fields[0].validators[1].message


def test_out_of_range_month_field():
    """Verify an out of range month is not allowed."""
    field = DateInputField()
    with pytest.raises(ValidationError) as err:
        field.clean(["11", "13", "2007"])
    error = err.value.args[0][0].args[0]
    assert error in field.fields[1].widget.errors
    assert error == field.fields[1].validators[2].message


def test_zero_value_month_field():
    """Verify a zero month is not allowed."""
    field = DateInputField()
    with pytest.raises(ValidationError) as err:
        field.clean(["11", "0", "2007"])
    error = err.value.args[0][0].args[0]
    assert error in field.fields[1].widget.errors
    assert error == field.fields[1].validators[1].message


def test_out_of_range_year_field():
    """Verify an out of range year is not allowed."""
    field = DateInputField()
    with pytest.raises(ValidationError) as err:
        field.clean(["11", "12", "999999999"])
    error = err.value.args[0][0].args[0]
    assert error in field.fields[2].widget.errors
    assert error == field.fields[2].validators[2].message


def test_zero_value_year_field():
    """Verify a zero year is not allowed."""
    field = DateInputField()
    with pytest.raises(ValidationError) as err:
        field.clean(["11", "12", "0"])
    error = err.value.args[0][0].args[0]
    assert error in field.fields[2].widget.errors
    assert error == field.fields[2].validators[1].message


def test_invalid_date_on_non_leap_year():
    """Verify an incorrect date on a non-leap year is not allowed."""
    field = DateInputField()
    with pytest.raises(ValidationError) as err:
        field.clean(["29", "2", "2007"])
    error = err.value.args[0][0]
    assert error == (
        "'29' is not a valid day for February 2007 - "
        "please enter a value between 1 and 28."
    )


def test_invalid_date_on_30_day_month():
    """Verify an incorrect date on a 30 day month is not allowed."""
    field = DateInputField()
    with pytest.raises(ValidationError) as err:
        field.clean(["31", "4", "2007"])
    error = err.value.args[0][0]
    assert error == (
        "'31' is not a valid day for April 2007 - "
        "please enter a value between 1 and 30."
    )
