==============
Torchbox Forms
==============

A Torchbox-flavoured template pack for `django-crispy-forms`_, allowing you to
generate consistent, usable and accessible forms in your Django projects.

.. _django-crispy-forms: https://github.com/maraujop/django-crispy-forms/

Requires Django 2.2 or later and django-crispy-forms 1.9 or later.


Quickstart
==========

This is a minimal 'how to' without options or details - see the
`tbxforms documentation <http://tbxforms.readthedocs.io/>`_ for full
instructions for installation and usage.

Install using pip::

    pip install tbxforms


Add django-crispy-forms and tbxforms to your installed apps::

    INSTALLED_APPS = [
      ...
      'crispy_forms',
      'tbxforms',
    ]

Now add the following settings to tell django-crispy-forms to use this theme::

    CRISPY_ALLOWED_TEMPLATE_PACKS = ["tbx"]
    CRISPY_TEMPLATE_PACK = "tbx"


Build a regular crispy form using layout objects from ``tbxforms``::

    from django import forms

    from tbxforms.helper import FormHelper
    from tbxforms.layout import Submit


    class TextInputForm(forms.Form):

        name = forms.CharField(
            label="Name",
            help_text="Your full name.",
            widget=forms.TextInput(),
            error_messages={
                "required": "Enter your name as it appears on your passport"
            }
        )

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.add_input(Submit("submit", "Submit"))


Render the form in your templates as normal::

    {% load crispy_forms_tags %}
    {% crispy form %}


Further reading
===============

* Read the documentation on `Read the docs`_
* Download the `PyPi package`_
* Learn more about `Django Crispy Forms`_

.. _Read the docs: http://tbxforms.readthedocs.io/
.. _PyPi package: http://pypi.python.org/pypi/tbxforms
.. _Django Crispy Forms: https://django-crispy-forms.readthedocs.io/en/latest/
