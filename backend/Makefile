
# run the fastapi app locally
run:
	poetry run fastapi run

# fixes linting and formatting issues, run tests
check: 	
	poetry run ruff format --line-length 120 .
	poetry run ruff check --line-length 120 --fix .
	poetry run pytest -v tests/



### Github Actions
format:
	poetry run ruff check --line-length 120 .

test:
	poetry run pytest -v tests/
