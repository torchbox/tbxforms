"""
Tests to verify form and formset errors show.
"""

from django.utils.html import mark_safe

import pytest

from tests.forms import CheckboxForm
from tests.utils import render_form


@pytest.fixture
def form():
    """
    A valid form to use as a base for all tests.
    """
    return CheckboxForm(data={"accept": True})


def test_no_error(self, form, snapshot_html):
    """
    Test default form used for tests is valid.
    """

    assert form.is_valid()
    assert render_form(form) == snapshot_html


def test_default_error_title(self, form, snapshot_html):
    """
    Test default error title shows if there's an error.
    """
    form.add_error(None, "An example non-field error.")
    assert not form.is_valid()

    rendered_form = render_form(form)
    assert rendered_form == snapshot_html
    assert "There is a problem with your submission" in rendered_form


def test_custom_error_title(self, form, snapshot_html):
    """
    Test custom error title shows if there's an error.
    """
    form.helper.form_error_title = "Uh-oh!"
    form.add_error(None, "An example non-field error.")
    assert not form.is_valid()

    rendered_form = render_form(form)
    assert rendered_form == snapshot_html
    assert "Uh-oh!" in rendered_form


def test_markup_allowed_in_non_field_error(self, form, snapshot_html):
    """
    Test markup is rendered for non-field errors.
    """
    form.add_error(None, mark_safe("Non-field error <i>with markup</i>."))
    assert not form.is_valid()

    rendered_form = render_form(form)
    assert rendered_form == snapshot_html
    assert "<i>with markup</i>" in rendered_form


def test_markup_allowed_in_field_error(self, form, snapshot_html):
    """
    Test markup is rendered for non-field errors.
    """
    form.add_error("accept", mark_safe("Field error <i>with markup</i>."))
    assert not form.is_valid()

    rendered_form = render_form(form)
    assert rendered_form == snapshot_html
    assert "<i>with markup</i>" in rendered_form
