from django.conf import settings
from django.utils.html import conditional_escape

from crispy_forms.layout import BaseInput


class Button(BaseInput):
    """
    Create a button of any type.

    Buttons are rendered by default as Design System primary buttons. When
    dealing with the basic objects you will need to pass the appropriate css
    class to get them to display as secondary or warning buttons.

    Examples: ::

        Button('add', 'Add contact')
        Button('cancel', 'Cancel', css_class="tbxforms-button--secondary")
        Button('delete', 'Delete user', css_class="tbxforms-button--warning")

    To save some typing there are class methods which save you the trouble of
    setting the css class: ::

        Button.primary('add', 'Add contact')
        Button.secondary('cancel', 'Cancel')
        Button.warning('delete', 'Delete user')

    Buttons are disabled by setting the disabled attribute to true: ::

        Button.primary('add', 'Add contact', disabled=True)

    Arguments:

        name (str): the value sent when the form is submitted.

        value (str): the button's title.

        disabled (bool, optional): is the button disabled. The default is
            ``False``.

        css_id (str, optional): an unique identifier for the <button>.
            Generally you will need to set this only if you need to add some
            javascript or very specific styling.

        css_class (str, optional): the names of one or more CSS classes that
            will be added to the <button>. The basic Design System CSS class,
            ``tbxforms-button`` is added automatically. This parameter is for
            any extra styling you want to apply.

        template (str, optional): the path to a template that overrides the
            one normally used.

        **kwargs: any additional attributes you want to add to the <button>.

    """

    template = "%s/layout/button.html"

    @classmethod
    def primary(cls, name, value, disabled=False, css_class="", **kwargs):
        """Create a primary button."""
        return Button(
            name,
            value,
            disabled=disabled,
            css_class=(
                f"{css_class} tbxforms-button tbxforms-button--primary"
            ),
            **kwargs,
        )

    @classmethod
    def secondary(cls, name, value, disabled=False, css_class="", **kwargs):
        """Create a secondary button."""
        return Button(
            name,
            value,
            disabled=disabled,
            css_class=(
                f"{css_class} tbxforms-button tbxforms-button--secondary"
            ),
            **kwargs,
        )

    @classmethod
    def warning(cls, name, value, disabled=False, css_class="", **kwargs):
        """Create a warning button."""
        return Button(
            name,
            value,
            disabled=disabled,
            css_class=(
                f"{css_class} tbxforms-button tbxforms-button--warning"
            ),
            **kwargs,
        )

    def __init__(self, name, value, disabled=False, css_class="", **kwargs):
        if disabled:
            kwargs["disabled"] = "disabled"
            kwargs["aria-disabled"] = "true"

        # Escape HTML within button `value`'s unless it's set to allow.
        # NB. Also see https://github.com/torchbox/tbxforms/blob/main/tbxforms/forms.py#L39  # noqa: E501
        if all(
            [
                value,
                not getattr(settings, "TBXFORMS_ALLOW_HTML_BUTTON", False),
            ]
        ):
            value = conditional_escape(value)

        self.css_class = css_class
        super().__init__(name, value, **kwargs)


class Submit(BaseInput):
    def __init__(self, name, value, disabled=False, css_class="", **kwargs):
        raise NotImplementedError(
            "'Submit' is not used in tbxforms in favour of a 'Button'. "
            "See README for an example."
        )
