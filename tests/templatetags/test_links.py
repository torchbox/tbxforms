"""
Tests to verify template tags for generating links are working.

"""
import os

from django.test.html import parse_html
from django.utils.safestring import SafeString

from tbxforms.templatetags.tbxforms import button_link
from tests.utils import (
    TEST_DIR,
    parse_contents,
)

RESULT_DIR = os.path.join(TEST_DIR, "templatetags", "results")


def test_button_link():
    html = button_link("http://www.example.com/", "Link")
    assert isinstance(html, SafeString)
    assert parse_html(html) == parse_contents(RESULT_DIR, "button_link.html")
