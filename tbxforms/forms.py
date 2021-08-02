class BaseForm:
    @staticmethod
    def conditional_fields_to_show_as_required() -> []:
        """
        Field names defined here will be shown as required fields (though they
        will not have the HTML5 required attribute).
        Actual validation of conditionally required fields will need manually
        adding via the form's `clean()` method.
        """
        return []

    class Media:
        js = ("js/tbxforms.js",)
