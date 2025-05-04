
# run the fastapi app locally
run:
	poetry run fastapi run

check: 	
	poetry run ruff format --line-length 120 .
	poetry run ruff check --line-length 120 --fix .
	poetry run pytest -v

test:
	poetry run pytest -n 4 tests/
