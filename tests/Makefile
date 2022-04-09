.DEFAULT_GOAL := test

clean:
	rm -rf ../build/reports/*

test:
	poetry run tox -e test

coverage-linting:
	poetry run tox -e coverage-linting

coverage-reports:
	poetry run tox -e coverage-reports

lint:
	make coverage-linting
	make coverage-reports

tox:
	poetry run tox
