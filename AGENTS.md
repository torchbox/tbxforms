# Repository Guidelines

## Project Structure & Module Organization

`tbxforms/` contains the Django package. Core Python modules live at the
package root, reusable layout objects are in `tbxforms/layout/`, template tags
are in `tbxforms/templatetags/`, Django templates are in
`tbxforms/templates/tbxforms/`, and source styles/scripts are in
`tbxforms/static/`. Tests mirror those areas under `tests/`, with snapshot HTML
fixtures in `tests/**/__snapshots__/`. Build outputs are written to `dist/` and
packaged static assets.

## Build, Test, and Development Commands

Use Poetry for Python environment management in this repository.

- `poetry install` installs Python dependencies.
- `npm install` installs frontend build and lint dependencies.
- `poetry run pytest` runs the test suite against the active environment.
- `poetry run tox` runs the supported Python/Django matrix from `tox.ini`.
- `poetry run pytest --snapshot-update` updates Syrupy snapshots after checking
  the rendered HTML change is intentional.
- `pre-commit run --all-files` runs Python, template, JS, and formatting checks.
- `npm run lint` runs ESLint and Prettier checks.
- `npm run build` builds the Vite bundle and copies Sass into `dist/`.

## Coding Style & Naming Conventions

Python uses Black and isort with a 79-character line length. Flake8 enforces the
same line length and a maximum complexity of 18. Use 4-space indentation for
Python, Sass, CSS, and Markdown; use 2 spaces for JavaScript, JSON, and YAML.
Django templates use `djlint` with the Django profile. Keep public layout and
field classes named descriptively, matching existing patterns such as
`Fieldset`, `Checkboxes`, and `DateInputField`.

## Testing Guidelines

Tests use pytest, Django test settings from `tests/settings.py`, and Syrupy for
HTML snapshots. Name test files `test_*.py` and place new coverage beside the
feature area, for example `tests/layout/test_select.py` for layout rendering.
For template output changes, review snapshot diffs before updating fixtures.
Run targeted pytest during development, then `poetry run tox` for compatibility
changes.

## Commit & Pull Request Guidelines

Recent history uses short, imperative commit subjects, often with GitHub PR
numbers, for example `Fix radios not including 'required' attribute when set as
required (#98)`. Keep commits focused. Pull requests should describe the change,
link the related issue when available, mention snapshot or visual changes, and
list the checks run. Include screenshots or rendered HTML examples when form
markup or styling changes.

## Agent-Specific Instructions

Start new work on a branch and ask for the branch name first. Prefer Poetry when
managing Python dependencies here, despite the general preference for UV in
non-Poetry projects.
