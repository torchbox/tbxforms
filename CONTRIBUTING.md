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

1. `npm run format`
2. `pre-commit`
3. Bump project version in pyproject.toml (do not update package.json as `np` will do this automatically)
4. `np --no-tests`
5. `poetry build`
6. `poetry publish -u {username}`
