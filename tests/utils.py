import io
import os

import django

from django.conf import settings as django_settings
from django.template import (
    Context,
    Template,
)
from django.test.html import parse_html

from bs4 import BeautifulSoup as soup
from syrupy.extensions.single_file import (
    SingleFileSnapshotExtension,
    WriteMode,
)

from . import settings


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
    return soup(
        Template(template).render(Context(kwargs)), "html.parser"
    ).prettify(formatter="html")


def render_form(form, **kwargs):
    """
    Render a form using a Django Template
    """
    context = Context(kwargs)
    context["form"] = form
    tpl = """
        {% load crispy_forms_tags %}
        {% crispy form %}
    """
    return soup(Template(tpl).render(context), "html.parser").prettify(
        formatter="html"
    )


class SingleHtmlFileExtension(SingleFileSnapshotExtension):
    """
    Custom syrupy snapshot extension that writes all snapshots to individual
    HTML files
    """

    _write_mode = WriteMode.TEXT
    _file_extension = "html"
