from django.core.management.base import BaseCommand, CommandError
import pandas as pd
from finance.models import Investment, Investor
from django.apps import apps


class Command(BaseCommand):
    help = "Load a investments csv file into the database"

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str, help="Path to the CSV file")
        parser.add_argument(
            "--model", type=str, help="Name of the model to import data into"
        )

    def create_investment(self, row_iter):
        objs = [
            Investment(
                id=row["id"],
                investor_id=Investor.objects.get(pk=row["investor_id"]),
                startup_name=row["startup_name"],
                invested_amount=row["invested_amount"],
                percentage_fees=row["percentage_fees"],
                date_added=row["date_added"],
                fees_type=row["fees_type"],
            )
            for index, row in row_iter
        ]

        Investment.objects.bulk_create(objs)
        self.stdout.write(self.style.SUCCESS("Investments imported successfully"))

    def create_investor(self, row_iter):
        objs = [
            Investor(
                id=row["id"],
                name=row["name"],
                address=row["address"],
                credit=row["credit"],
                phone=row["phone"],
                email=row["email"],
            )
            for index, row in row_iter
        ]

        Investor.objects.bulk_create(objs)
        self.stdout.write(self.style.SUCCESS("Investors imported successfully"))

    def handle(self, *args, **kwargs):
        csv_file = kwargs["path"]
        model_name = kwargs["model"]
        try:
            df = pd.read_csv(csv_file)
            row_iter = df.iterrows()
            if model_name == "investment":
                self.create_investment(row_iter)
            elif model_name == "investor":
                self.create_investor(row_iter)
            else:
                raise CommandError("Invalid model name provided")

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(
                    "File not found. Please provide a valid CSV file path."
                )
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
