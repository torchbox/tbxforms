# Contribution Guidelines

Thank you for considering to help this project.

We welcome all support, whether on bug reports, code, design, reviews, tests, documentation, and more.

## Development

### Installation

With Python 3.8 or up, Node 16, [pre-commit](https://pre-commit.com/) and [Poetry 1.4.1](https://python-poetry.org/docs/#installing-with-the-official-installer)

```bash
git clone git@github.com:torchbox/tbxforms.git
cd tbxforms/
poetry install
pre-commit install
npm install
```

### Python testing

Run the Python tests with `poetry run pytest`.

If your changes cause snapshot tests to fail, verify that the changes you have caused are expected. Update the snapshots with `poetry run pytest --snapshot-update`.

## Publishing

1. `pre-commit` - run linters
2. `pytest` - run backend tests
3. Bump project version in pyproject.toml and package.json
4. Update CHANGELOG headings (add a new heading beneath the "Unreleased" heading)
5. `poetry lock --no-update` - Lock python packages
6. `npm i --package-lock-only` - Lock javascript packages
7. `npm run build` - build NPM package
8. `poetry build` - build python package
9. `npm publish` - publish package to npmjs.com
10. `poetry publish` - publish package to pypi.org
11. Create a [release](https://github.com/torchbox/tbxforms/releases) with relevant changelog entries and upgrade considerations
