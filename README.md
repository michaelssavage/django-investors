# oneragtime-challenge

## Excel Book

The supplied data for creating the Modal is in oneragtime.xlsx.

## Running the database with docker

Spin up a Postgres database with `./scripts/start-dev-db.sh`

## Initial Data Loading

There are investors and investments fixtures available for populating the data.

Just run: `python manage.py loaddata fixtures/*.json`
