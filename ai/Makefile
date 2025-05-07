check: 
	poetry run ruff format --line-length 120 .
	poetry run ruff check --line-length 120 . --fix



### Github Actions
format:
	poetry run ruff check --line-length 120 .

test:
	poetry run pytest -n 4
