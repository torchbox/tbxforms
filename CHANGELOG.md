# Changelog

> All notable changes to this project will be documented in this file. This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Types of changes

-   `Added` for new features.
-   `Changed` for changes in existing functionality.
-   `Deprecated` for soon-to-be removed features.
-   `Dev` for changes to the developer experience.
-   `Fixed` for bug fixes.
-   `Removed` for now removed features.
-   `Security` in case of vulnerabilities.

## Unreleased

### Added

-   Template linting to CI using `djlint`
-   Snapshot formatting check to CI using `djlint`
-   Autoformatting of snapshots using `djlint`
-   Testing across Django versions 2.2 - 4.0 and Python versions 3.8 - 3.11 using `tox`
-   Support for dividers on checkbox fields

### Changed

-   Use snapshot testing plugin (syrupy) for component rendering tests instead of HTML fixtures
-   form.helper (`FormHelper`) changed from a static `@property` to the form's `__init__` method to allow changes at runtime.

### Fixed

-   `Field.select` label size and tag can be changed.
-   `DateInputField` raises a `ValidationError` (instead of `ValueError`) when given invalid input
