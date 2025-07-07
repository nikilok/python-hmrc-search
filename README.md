# python-hmrc-search

## Install

- set up an enviornment with pip or conda and activate it.
- install poetry the dependency manager `curl -sSL https://install.python-poetry.org | python3 -`
- install the packages `poetry install` or update them if installed using `poetry update`

## Steps to start

- start for development - `poetry run fastapi dev app/main.py`
- start for production - `poetry run fastapi run app/main.py`

## Format

`poetry run black .`

## Sort imports

`poetry run isort .`

## Lint

`poetry run flake8 .`

<img width="495" alt="image" src="https://github.com/user-attachments/assets/4a5fa7a5-0c20-480e-8f15-00dfd9c72b2e" />
<img width="802" alt="image" src="https://github.com/user-attachments/assets/5d3dc009-9dce-41bd-b4c9-c660a7c594ad" />

automatic swagger docs at http://localhost:8000/docs
<img width="1647" alt="image" src="https://github.com/user-attachments/assets/0e79bfd9-6cbc-454e-8b82-476e60ed887f" />

