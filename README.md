## Vinny    

### Instructions on setting up environment (on Windows):

Perform the following commands in a terminal at the project root level.

- Use `python -m venv .venv` to generate a virtual environment.

- Use `. .venv/scripts/Activate` to activate the environment.

- Use `pip install poetry` to get poetry.

- Use `poetry install` to install all packages required for the project.

### Running the service

- Use `python -m main` to run the transcription service.

- Use `python -m server` to run the flask frontend app from the server folder.

Exit manually using control-c.

### Clean Code

- Use `poetry run mypy .` to check types are ok.

- Use `poetry run blue .` to automatically fix formatting (PEP-8 etc.)

- Use `potry run isort .` to order and group imports.

- Use `poetry run pylint core tests server main.py` to run linting.

### Testing

- Use `poetry run pytest` to run tests.