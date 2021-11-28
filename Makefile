load:
	flask load sample.csv

shell:
	FLASK_DEBUG=1 flask shell

debug_server:
	FLASK_DEBUG=1 flask run

prod_server:
	flask run

export_requirements:
	poetry export --output=requirements.txt

install_dependencies:
	poetry install