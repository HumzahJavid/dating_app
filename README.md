# dating_app
# Badges
![ci-workflow](https://github.com/HumzahJavid/dating_app/actions/workflows/ci-workflow.yml/badge.svg)


## Development setup
Poetry is used as the virtual env/ package manager


See poetry install guide: https://python-poetry.org/docs/master/#installing-with-the-official-installer


Once ready to use poetry. Ensure all the requirments are installed

`poetry install`



### Using pre-commit
This repo comes with pre-commit (as a poetry dependancy).

To run pre-commit on staged files:

`poetry run pre-commit run`

To run pre-commit on all files:

`poetry run pre-commit run --all-files`




### Running automated tests and linting report jobs

The `Makefile` in the `./tests` directory is designed to make running tests easier.

**Run test**
 - `make` or `make test`.

**Run lint jobs and generate report**
 - `make lint` (generated reports in `build/reports`)

 - `make clean` (cleans the `build/reports` directory)
