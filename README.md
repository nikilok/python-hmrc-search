# python-hmrc-search

## Install

- set up an enviornment with pip or conda and activate it.
- install poetry the dependency manager `curl -sSL https://install.python-poetry.org | python3 -`
- install the packages `poetry install` or update them if installed using `poetry update`

## Steps to start

- start - `poetry run fastapi dev app/main.py`
- start for production - `poetry run uvicorn app.main:app --reload`
