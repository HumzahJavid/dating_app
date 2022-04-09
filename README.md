# dating_app


# Development setup
Poetry is used as a virtual env/ package manager


See poetry install guide: https://python-poetry.org/docs/master/#installing-with-the-official-installer


Once ready to use poetry. Ensure all the requirments are installed

`poetry install`


###

### Using pre-commit
This repo comes with pre-commit (as a poetry dependancy).

To run pre-commit on staged files:

`poetry run pre-commit run`

To run pre-commit on all files:

`poetry run pre-commit run --all-files`
