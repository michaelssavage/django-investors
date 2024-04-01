# oneragtime-challenge

## Excel Book

The supplied data for creating the Modal is in oneragtime.xlsx.

## Running the database with docker

Spin up a Postgres database with `./scripts/start-dev-db.sh`

## Initial Data Loading

Add the investments.csv and investors.csv to the root of the project, then run these:

`python manage.py populate_data --path investor.csv --model investor`

## Run the app

`python manage.py runserver`
