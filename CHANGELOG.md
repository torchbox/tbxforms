# Changelog

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Types of changes

-   `Added` for new features.
-   `Changed` for changes in existing functionality.
-   `Deprecated` for soon-to-be removed features.
-   `Developer` for changes to the developer experience.
-   `Fixed` for bug fixes.
-   `Pinned packages updated` to list pinned packages that have been updated. Do not write changelog entries for third-party dependencies.
-   `Removed` for now removed features.

## Unreleased

## [4.3.0](https://github.com/torchbox/tbxforms/releases/tag/v4.3.0)

### Added

-   Allow per-form override of `settings.TBXFORMS_HIGHLIGHT_REQUIRED_FIELDS` [#97]

## [4.2.0](https://github.com/torchbox/tbxforms/releases/tag/v4.2.0)

### Fixed

-   Conditional fields not working when applied to field objects (e.g. `Field.text`, `Field.checkboxes`) instead of container objects (e.g. `Div`, `Fieldset`) [#95]

## [4.1.0](https://github.com/torchbox/tbxforms/releases/tag/v4.1.0)

### Added

-   Error summary can be hidden [#93]

### Changed

-   Small tweak to fieldset styles [#93]

## [4.0.0](https://github.com/torchbox/tbxforms/releases/tag/v4.0.0)

### Changed

-   Renamed `tbx` template directory and crispy forms template pack to `tbxforms` [#92]

### Fixed

-   Conditional fields not working properly when there are multiple elements inspecting the same driving field [#91]

### Removed

-   IE11 support [#91]

## [3.0.0](https://github.com/torchbox/tbxforms/releases/tag/v3.0.0)

### Developer

-   Guidance on how to update `govuk-frontend` [#80]

### Pinned packages updated

-   `govuk-frontend` from 3.13.0 (possibly) to 5.4.1 [#80]

### Removed

Several CSS classes/mixins have been removed/renamed in this release, some of
which are vendor changes in `govuk-frontend`.

Unfortunately, the initial release of tbxforms customised the styles from
`govuk-frontend` without documentation - including which version was used as a
base. As a result, it's hard to distinguish between variables/mixins we
added which have now been removed and those which GDS have removed over time.

However, variables which have now been removed from our \_variables.scss are:

-   `$tbxforms-border-colour-conditional` (no longer configurable; now using GDS' `$tbxforms-border-colour`) [#80]
-   `$tbxforms-border-width-conditional` (no longer configurable; now using GDS' `$tbxforms-border-width`) [#80]
-   `$tbxforms-weight--bold` (use `$tbxforms-font-weight-bold` instead) [#80]
-   `$tbxforms-weight--normal` (use `$tbxforms-font-weight-regular` instead) [#80]
-   `$tbxforms-grid` (no longer configurable; now using GDS' default spacing) [#80]
-   `$tbxforms-spacer` (no longer configurable; now using GDS' default spacing) [#80]
-   `$tbxforms-in-field-spacer` (no longer configurable; now using GDS' default spacing) [#80]
-   `$tbxforms-form-group-spacer` (no longer configurable; now using GDS' default spacing) [#80]
-   `$tbxforms-base-font-size` (use `$tbxforms-typography-scale` instead) [#80]
-   `$tbxforms-base-line-height` (use `$tbxforms-typography-scale` instead) [#80]
-   `$tbxforms-font-sizes` (use `$tbxforms-typography-scale` instead) [#80]

## [2.1.0](https://github.com/torchbox/tbxforms/releases/tag/v2.1.0)

### Changed

-   Allow required fields to be highlighted instead of optional ones [#78]
-   Allow markup in error messages [#79]

### Fixed

-   Choice hints not showing on Django 5.x [#69]

## [2.0.1](https://github.com/torchbox/tbxforms/releases/tag/v2.0.1)

### Pinned packages updated

-   `vite` from 2.9.17 to 2.9.18 [#77]
-   `black` from 22.3.0 to 24.3.0 [#77]
-   `poetry` from 1.7.1 to 1.8.3 [#77]

## [2.0.0](https://github.com/torchbox/tbxforms/releases/tag/v2.0.0)

### Added

-   Python support for 3.12 [#61]
-   Django support for 4.1 and 4.2 [#61]

### Changed

-   `|safe` is no longer applied within templates [#61]

### Removed

-   Django support for 2.2, 3.0, and 3.1 [#61]
-   `TBXFORMS_ALLOW_HTML_LABEL`, `TBXFORMS_ALLOW_HTML_HELP_TEXT`, and `TBXFORMS_ALLOW_HTML_BUTTON` settings (developers must now mark strings as safe to render markup) [#61] [#62]
-   `sass` support for <1.33.0 [#60]

### Fixed

-   Documentation referencing an incorrect CSS import path

### Pinned packages updated

-   `django` from 2.2.x to 3.2.x [#61]
-   `django-crispy-forms` from 1.13.x to 2.1.x [#61]
-   `flake8` from 4.0.1 to 5.0.4 [#61]

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
