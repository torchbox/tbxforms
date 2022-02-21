# Contribution Guidelines

Thank you for considering to help this project.

We welcome all support, whether on bug reports, code, design, reviews, tests, documentation, and more.

## Development

### Installation

With Python 3.8 or up, Node 16, and [pre-commit](https://pre-commit.com/),

```bash
git clone git@github.com:torchbox/tbxforms.git
cd tbxforms/
pip install poetry==1.1.13
poetry install
pre-commit install
npm install
```

### Publishing

1. `pre-commit` - run linters
2. `pytest` - run backend tests
3. Bump project version in pyproject.toml and package.json
4. `poetry lock --no-update` - Lock python packages
5. `npm i --package-lock-only` - Lock javascript packages
6. `npm run build` - build NPM package
7. `poetry build` - build python package
8. `npm publish` - publish package to npmjs.com
9. `poetry publish` - publish package to pypi.org
