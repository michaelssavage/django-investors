from datetime import UTC, datetime
import re
from django.core.management.base import BaseCommand, CommandError
import pandas as pd
from finance.models import Bill, CashCall, Investment, Investor
from finance.utils import BILL_EXISTS_WARNING, CASH_CALL_EXISTS_WARNING


class Command(BaseCommand):
    help = "Create cash calls when investors and investments are available"

    def create_cashcalls(self):
        investments = Investment.objects.all()
        if not investments:
            self.stdout.write(
                self.style.ERROR("Please add investments before generating bills.")
            )
            return
        for investment in investments:
            existing_bill = Bill.objects.filter(
                investor_id=investment.investor_id, investment_id=investment
            ).exists()
            if existing_bill:
                self.stdout.write(self.style.ERROR(BILL_EXISTS_WARNING))
                return

            fee = investment.generate_bill()
            now = datetime.now(UTC)

            Bill.objects.create(
                investor_id=investment.investor_id,
                investment_id=investment,
                fees_amount=fee,
                date_added=now,
                fees_type=investment.fees_type,
            )

        self.stdout.write(self.style.SUCCESS("Bills created."))
        investors = Investor.objects.all()
        bills = Bill.objects.all()
        for investor in investors:
            bills = Bill.objects.filter(investor_id=investor)
            total_amount = sum([bill.fees_amount for bill in bills])
            now = datetime.now(UTC)

            ibanRegex = r"\b(\d{16})\b"
            match = re.search(ibanRegex, investor.credit)
            if match:
                iban = match.group(1)
            else:
                iban = investor.credit
            existing_cash_call = CashCall.objects.filter(
                total_amount=total_amount, IBAN=iban, email_send=investor.email
            ).exists()
            if existing_cash_call:
                self.stdout.write(self.style.ERROR(CASH_CALL_EXISTS_WARNING))

            CashCall.objects.create(
                total_amount=total_amount,
                IBAN=iban,
                email_send=investor.email,
                date_added=now,
                invoice_status="Pending",
            )

        self.stdout.write(self.style.SUCCESS("Cash Calls created."))

    def handle(self, *args, **kwargs):
        try:
            self.create_cashcalls()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
