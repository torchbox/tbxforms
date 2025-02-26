# Contribution Guidelines

Thank you for considering to help this project.

We welcome all support, whether on bug reports, code, design, reviews, tests, documentation, and more.

## Development

### Installation

With Python 3.8+, Node 20, and [Poetry 1.8.3](https://python-poetry.org/docs/#installing-with-the-official-installer) installed, run:

```bash
git clone git@github.com:torchbox/tbxforms.git
cd tbxforms/
poetry install
pre-commit install
npm install
```

### Testing

This project uses [pytest 7.0.x](https://docs.pytest.org/en/7.0.x/) and [tox](https://github.com/tox-dev/tox) for backend testing.

Generally you should use `tox`, though for quick testing during development you may want to just run `pytest` for ease.

#### Run tests using single package versions

`poetry run pytest` will run tests in whatever Python/package versions you have activated/installed.

#### Run tests against all supported package versions

`poetry run tox` will run tests against our supported package matrix.

#### Updating snapshots

If your changes cause the snapshot tests to fail:

1. Verify that the changes you have caused are expected - don't just blindly update the snapshots, they're there for a reason.
2. Run `poetry run pytest --snapshot-update` to update the snapshots.

#### Testing `tbxforms` in a real-world project

`tbxforms` can also be published to https://test.pypi.org/project/tbxforms/ to
make it easier to test changes to the package within a real-world project.

##### Publishing to test.pypi

To publish a new version of `tbxforms` to test.pypi:

1. Set an alpha version in `pyproject.toml` (e.g. `version = "4.3.0-alpha.1"`)
2. Run `poetry publish --repository testpypi` to push the new version to test.pypi

##### Installing the alpha/test version

To install the alpha/test version of `tbxforms`, run:

```bash
# Using poetry
poetry add tbxforms --index-url https://test.pypi.org/simple/

# Using pip
pip install --index-url https://test.pypi.org/simple/ --no-deps tbxforms
```

(note, you may need to clear your project's poetry cache if Poetry cannot find the latest version: `poetry cache clear --all .`)

## Publishing

1. `pre-commit run --all-files` - run linters
2. `poetry run tox` - run backend tests against our supported package matrix.
3. Bump project version in pyproject.toml and package.json
4. Update CHANGELOG headings (add a new heading beneath the "Unreleased" heading)
5. `poetry lock --no-update` - Lock python packages
6. `npm i --package-lock-only` - Lock javascript packages
7. Commit changes to `main`
8. Tag release commit (e.g. `v4.2.0`)
9. Push changes and tag to `main`
10. `npm run build` - build NPM package
11. `poetry build` - build python package
12. `npm publish` - publish package to npmjs.com
13. `poetry publish` - publish package to pypi.org
14. Create a [release](https://github.com/torchbox/tbxforms/releases) with relevant changelog entries and upgrade considerations

## Common tasks

### Updating govuk-frontend

Everything within the `/static/sass/govuk/` directory is mostly unmodified,
except that:

1. all instances of "govuk-" have been replaced with "tbxforms-"
2. unused .scss files and all other file types (.js, .md, .njk) have been deleted
3. imports to unused .scss files have been commented-out (not removed, to make tracing changes easier)
4. added `calc()` to equations to avoid Dart Sass 2.0.0 deprecation warning

There's also some overrides in `/static/sass/govuk-overrides/` to be aware of.

This list also acts as a checklist for updating [govuk-frontend](https://github.com/alphagov/govuk-frontend) in the future.
