# Contribution Guidelines

Thank you for considering to help this project.

We welcome all support, whether on bug reports, code, design, reviews, tests, documentation, and more.

## Development

### Installation

With Python 3.7 or up, Node 16, and [pre-commit](https://pre-commit.com/),

```bash
git clone git@github.com:kbayliss/tbxforms.git
cd tbxforms/
poetry install
pre-commit install
npm install
npm run build
```

### Publishing

1. `npm run format` - run FE linters
2. `pre-commit` - run BE linters (and some FE ones)
3. Bump project version in pyproject.toml and package.json
4. `npm run build` - build NPM package
5. `poetry build` - build python package
6. `npm publish` - publish package to npmjs.com
7. `poetry publish` - publish package to pypi.org
