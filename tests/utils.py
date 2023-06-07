import io
import os

import django

from django.conf import settings as django_settings
from django.template import (
    Context,
    Template,
)
from django.test.html import parse_html

import djlint

from crispy_forms.utils import render_crispy_form
from syrupy.extensions.single_file import (
    SingleFileSnapshotExtension,
    WriteMode,
)

from . import settings

DJLINT_CONF = djlint.settings.Config(
    src="-",
    configuration=(
        os.path.abspath(os.path.join(__file__, "../pyproject.toml"))
    ),
)


def configure_django(**kwargs):
    """
    Configure Django with all the settings defined in tests/settings.py.
    """
    values = {k: getattr(settings, k) for k in dir(settings) if k.isupper()}
    values.update(kwargs)
    django_settings.configure(**values)
    django.setup()


def get_contents(*args):
    with io.open(os.path.join(*args), "r", encoding="utf-8") as fp:
        return fp.read()


def parse_contents(*args):
    return parse_html(get_contents(*args))


def render_template(template, **kwargs):
    """
    Render a Django Template
    """
    return djlint.reformat.formatter(
        DJLINT_CONF, Template(template).render(Context(kwargs))
    )


def render_form(form, **kwargs):
    """
    Render a form as the `crispy' template tag does
    """
    return djlint.reformat.formatter(
        DJLINT_CONF, render_crispy_form(form, context=kwargs)
    )


class SingleHTMLFileExtension(SingleFileSnapshotExtension):
    """
    Custom syrupy snapshot extension that writes all snapshots to individual
    HTML files
    """

    _write_mode = WriteMode.TEXT
    _file_extension = "html"
