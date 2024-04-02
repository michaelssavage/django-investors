# oneragtime-challenge

This Django app automates the creation of cash calls for an investor. A cash call is an invoice consisting of a group bills. Generated bills and cash calls are stored in PostgreSQL.

Once cash calls are validated, an PDF invoice is generated.

Notion was used for jotting initial assumptions, and Trello was used for tracking work.

## Setup

You need docker-compose and a virtual environment. Create a new venv by running `python -m venv ./venv`.

Install the requirements by activating the venv and running `pip install -r requirements.txt`

## Running the database with docker

Spin up a Postgres database by running `./scripts/start-dev-db.sh`

## Run the app

You can then start the server by running `python manage.py runserver` and visiting `http://127.0.0.1:8000/`.

## Initial Data Loading

Add the investments.csv and investors.csv to the database by running `./scripts/load-postgres-data.sh`

You now have the option of adding the cash calls from the GUI or by script.

#### 1. Script

Run `./scripts/create-cash-calls-data.sh` to generate bills and cash calls. You can view the changes in the GUI when you refresh the page.

#### 2. GUI

You can create cash calls in the GUI at `http://127.0.0.1:8000/` by clicking the Generate All Bills button then clicking the Generate All Cash Calls button.
