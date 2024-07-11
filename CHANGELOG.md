# Changelog

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Types of changes

-   `Added` for new features.
-   `Changed` for changes in existing functionality.
-   `Deprecated` for soon-to-be removed features.
-   `Developer` for changes to the developer experience.
-   `Fixed` for bug fixes.
-   `Removed` for now removed features.
-   `Security` in case of vulnerabilities.

## Unreleased

## [2.0.0](https://github.com/torchbox/tbxforms/releases/tag/v2.0.0)

### Added

-   Python support for 3.12 [#61]
-   Django support for 4.1 and 4.2 [#61]

### Changed

-   `django-crispy-forms` updated to 2.1.x [#61]

### Deprecated

-   Django support for 2.2, 3.0, and 3.1 [#61]
-   `TBXFORMS_ALLOW_HTML_LABEL`, `TBXFORMS_ALLOW_HTML_HELP_TEXT`, and `TBXFORMS_ALLOW_HTML_BUTTON` settings (developers must now mark strings as safe to render markup) [#61] [#62]
-   `sass` support for <1.33.0 [#60]

### Fixed

-   Documentation referencing an incorrect CSS import path

### Security

-   `|safe` is no longer applied within templates [#61]

## [1.1.0](https://github.com/torchbox/tbxforms/releases/tag/v1.1.0)

### Added

-   Support for dividers on checkbox fields

### Changed

-   form.helper (`FormHelper`) changed from a static `@property` to the form's `__init__` method to allow changes at runtime
-   Update documentation and examples to use `Field` subclass methods (e.g. `Field.select`) to avoid passing `context` dictionary to `Field` (https://crispy-forms-gds.readthedocs.io/en/latest/reference/layout/field.html)
-   `BaseForm` renamed to `TbxFormsMixin` to more accurately convey what it is
-   Styles no longer depend on the form having the `.tbxforms` class

### Developer

-   Template linting to CI using `djlint`
-   Snapshot formatting check to CI using `djlint`
-   Autoformatting of snapshots using `djlint`
-   Testing across Django versions 2.2 - 4.0 and Python versions 3.8 - 3.11 using `tox`
-   Use snapshot testing plugin (syrupy) for component rendering tests instead of HTML fixtures

### Fixed

-   `Field.select` label size and tag can be changed
-   `DateInputField` no longer raises a `ValueError` when given invalid input (a `ValidationError` is raised instead)
-   `DateInputField` with `required=False` no longer raises a `ValueError` when no values are passed
-   `DateInputField` no longer errors with `OverflowError` when large values are passed
