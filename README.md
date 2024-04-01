# oneragtime-challenge

```
Requirements: django, docker-compose, pandas
```

## Running the database with docker

Spin up a Postgres database by running `./scripts/start-dev-db.sh`

## Initial Data Loading

Add the investments.csv and investors.csv to the database by running `./scripts/load-postgres-data.sh`

## Run the app

`python manage.py runserver`
