# dating_app
## Badges
![ci-workflow](https://github.com/HumzahJavid/dating_app/actions/workflows/ci-workflow.yml/badge.svg)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)

<!-- local badge -->
<!-- ![pylint rating](build/badges/rating.svg) -->
<!-- hosting on heroku (untested storage time)-->
<!-- ![pylint heroku ](https://heroku.herokuapp.com/badges/rating.svg) -->
![pylint-rating](https://raw.githubusercontent.com/HumzahJavid/humzahjavid/badges/badges/rating.svg)
![coverage](https://raw.githubusercontent.com/HumzahJavid/humzahjavid/badges/badges/coverage.svg)

![lint_errors](https://raw.githubusercontent.com/HumzahJavid/humzahjavid/badges/badges/lint_errors.svg)
![lint_failures](https://raw.githubusercontent.com/HumzahJavid/humzahjavid/badges/badges/lint_failures.svg)
![lint_total](https://raw.githubusercontent.com/HumzahJavid/humzahjavid/badges/badges/lint_total.svg)

![tests_errors](https://raw.githubusercontent.com/HumzahJavid/humzahjavid/badges/badges/tests_errors.svg)
![tests_failures](https://raw.githubusercontent.com/HumzahJavid/humzahjavid/badges/badges/tests_failures.svg)
![tests_skipped](https://raw.githubusercontent.com/HumzahJavid/humzahjavid/badges/badges/tests_skipped.svg)
![tests_total](https://raw.githubusercontent.com/HumzahJavid/humzahjavid/badges/badges/tests_total.svg)

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
