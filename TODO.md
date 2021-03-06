# To-do

- ~~Add more flake8 extensions to~~

  - ~~Poetry~~
  - ~~Nox lint sessions~~

- ~~Add more pre-commit hooks (like Prettier)~~

  - ~~Prettier~~
  - ~~isort~~
  - ~~doc8~~

- ~~Add Dependabot~~
- ~~Add some more mypy options~~

- ~~Add doc8 to nox~~
- GH issue template
- Sphinx theme

## Updates

- Switch isort to isort[pyproject] when flake8-isort can pick up on those settings
- Slowly move everything to pyproject as support is added

  - isort
  - mypy

- Update pytype to 2.8
- Update doc linters to numpy
- Switch isort to black_isort when (if?) it releases
- Try to upload to Read the Doc via a GitHub action
  [once supported](https://github.com/readthedocs/readthedocs.org/issues/1083).
