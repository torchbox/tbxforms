# Contribution Guidelines

Thank you for considering to help this project.

We welcome all support, whether on bug reports, code, design, reviews, tests, documentation, and more.

## Development

### Installation

With Python 3.8 or up, Node 20, [pre-commit](https://pre-commit.com/), and [Poetry 1.8.3](https://python-poetry.org/docs/#installing-with-the-official-installer)

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

## Publishing

1. `pre-commit run --all-files` - run linters
2. `poetry run tox` - run backend tests against our supported package matrix.
3. Bump project version in pyproject.toml and package.json
4. Update CHANGELOG headings (add a new heading beneath the "Unreleased" heading)
5. `poetry lock --no-update` - Lock python packages
6. `npm i --package-lock-only` - Lock javascript packages
7. `npm run build` - build NPM package
8. `poetry build` - build python package
9. `npm publish` - publish package to npmjs.com
10. `poetry publish` - publish package to pypi.org
11. Create a [release](https://github.com/torchbox/tbxforms/releases) with relevant changelog entries and upgrade considerations
