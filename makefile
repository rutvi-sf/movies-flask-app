test:
	pipenv run python -m pytest -s

run:
	pipenv run flask run

db-upgrade:
	pipenv run flask db upgrade

db-makemigrations:
	pipenv run flask db migrate
