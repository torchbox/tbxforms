"""
Tests to verify buttons are rendered correctly.

"""
from tbxforms.layout import Button
from tests.utils import render_template

TEMPLATE = '{% include "tbx/layout/button.html" %}'


def test_primary_button(snapshot_html):
    button = Button.primary("name", "Title")
    assert render_template(TEMPLATE, input=button) == snapshot_html


def test_secondary_button(snapshot_html):
    button = Button.secondary("name", "Title")
    assert render_template(TEMPLATE, input=button) == snapshot_html


def test_warning_button(snapshot_html):
    button = Button.warning("name", "Title")
    assert render_template(TEMPLATE, input=button) == snapshot_html


def test_disabled_button(snapshot_html):
    button = Button.primary("name", "Title", disabled=True)
    assert render_template(TEMPLATE, input=button) == snapshot_html


def test_css_class(snapshot_html):
    button = Button.primary("name", "Title", css_class="extra-css-class")
    assert render_template(TEMPLATE, input=button) == snapshot_html


def test_css_id(snapshot_html):
    button = Button.primary("name", "Title", css_id="new_id")
    assert render_template(TEMPLATE, input=button) == snapshot_html


def test_extra_attributes(snapshot_html):
    button = Button.primary("name", "Title", key="value")
    assert render_template(TEMPLATE, input=button) == snapshot_html
