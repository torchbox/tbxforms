"""
Tests to verify buttons are rendered correctly.

"""
import os

from django.utils.html import mark_safe

from tbxforms.layout import Button
from tests.utils import (
    TEST_DIR,
    parse_contents,
    parse_template,
)

RESULT_DIR = os.path.join(TEST_DIR, "layout", "results", "buttons")
TEMPLATE = '{% include "tbx/layout/button.html" %}'


def test_primary_button():
    button = Button.primary("name", mark_safe("Title<br>"))
    assert parse_template(TEMPLATE, input=button) == parse_contents(
        RESULT_DIR, "primary.html"
    )


def test_primary_button_incorrect_escaping():
    """Without mark_safe the result shouldn't be equal, see test_primary_button
    for the correct test case using the same template."""
    button = Button.primary("name", "Title<br>")
    assert parse_template(TEMPLATE, input=button) != parse_contents(
        RESULT_DIR, "primary.html"
    )


def test_secondary_button():
    button = Button.secondary("name", "Title")
    assert parse_template(TEMPLATE, input=button) == parse_contents(
        RESULT_DIR, "secondary.html"
    )


def test_warning_button():
    button = Button.warning("name", "Title")
    assert parse_template(TEMPLATE, input=button) == parse_contents(
        RESULT_DIR, "warning.html"
    )


def test_disabled_button():
    button = Button.primary("name", "Title", disabled=True)
    assert parse_template(TEMPLATE, input=button) == parse_contents(
        RESULT_DIR, "disabled.html"
    )


def test_css_class():
    button = Button.primary("name", "Title", css_class="extra-css-class")
    assert parse_template(TEMPLATE, input=button) == parse_contents(
        RESULT_DIR, "css_class.html"
    )


def test_css_id():
    button = Button.primary("name", "Title", css_id="new_id")
    assert parse_template(TEMPLATE, input=button) == parse_contents(
        RESULT_DIR, "css_id.html"
    )


def test_extra_attributes():
    button = Button.primary("name", "Title", key="value")
    assert parse_template(TEMPLATE, input=button) == parse_contents(
        RESULT_DIR, "attributes.html"
    )
