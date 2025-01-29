"""
Tests to verify buttons are rendered correctly.
"""

import pytest

from tbxforms.layout import Button
from tests.utils import render_template


@pytest.mark.parametrize(
    ("button_factory"),
    (
        (Button.primary),
        (Button.secondary),
        (Button.warning),
    ),
)
class TestButtons:
    TEMPLATE = '{% include "tbxforms/layout/button.html" %}'

    def test_button(self, button_factory, snapshot_html):
        button = button_factory("name", "Title")
        assert render_template(self.TEMPLATE, input=button) == snapshot_html

    def test_disabled_button(self, button_factory, snapshot_html):
        button = button_factory("name", "Title", disabled=True)
        assert render_template(self.TEMPLATE, input=button) == snapshot_html

    def test_css_class(self, button_factory, snapshot_html):
        button = button_factory("name", "Title", css_class="extra-css-class")
        assert render_template(self.TEMPLATE, input=button) == snapshot_html

    def test_css_id(self, button_factory, snapshot_html):
        button = button_factory("name", "Title", css_id="new_id")
        assert render_template(self.TEMPLATE, input=button) == snapshot_html

    def test_extra_attributes(self, button_factory, snapshot_html):
        button = button_factory("name", "Title", key="value")
        assert render_template(self.TEMPLATE, input=button) == snapshot_html
