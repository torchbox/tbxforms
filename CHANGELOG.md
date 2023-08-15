# Changelog

> All notable changes to this project will be documented in this file. This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Changed

-   Use snapshot testing plugin (syrupy) for component rendering tests instead of HTML fixtures

### Added

-   Template linting to CI using `djlint`
-   Snapshot formatting check to CI using `djlint`
-   Autoformatting of snapshots using `djlint`
-   Testing accross Django versions 2.2 - 4.0 and Python versions 3.8 - 3.11 using `tox`
-   Support for dividers on checkbox fields

### Fixed

-   `DateInputField` raises a `ValidationError` (instead of `ValueError`) when given invalid input
