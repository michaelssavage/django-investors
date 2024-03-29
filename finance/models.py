from datetime import datetime
from django.db import models

PAYMENT_CHOICES = [
    ("upfront", "Upfront"),
    ("yearly", "Yearly"),
]

INVOICE_STATUS_CHOICES = [
    ("Pending", "Pending"),
    ("Validated", "Validated"),
    ("Sent", "Sent"),
    ("Paid", "Paid"),
    ("Overdue", "Overdue"),
]

POINT_TWO_PERCENT = 0.002
POINT_FIVE_PERCENT = 0.005
ONE_PERCENT = 0.01
FEE_UPDATE_DATE = datetime(2019, 4, 1)
LARGE_INVESTMENT_THRESHOLD = 50000
MEMBERSHIP_FEE = 3000


def getYearsSincePurchase(date_val: datetime):
    return round((datetime.now() - date_val).days / 365)


def getDayOfYearPercentage(date_val: datetime):
    value = date_val.timetuple().tm_yday
    return 1 if value > 365 else round((value / 365), 2)


def addPre2019Fees(date_val: datetime, invested_amount: int, percentage_fees: int):
    fee: float = 0

    # initial fee
    fee += getDayOfYearPercentage(date_val) * invested_amount * percentage_fees

    for _ in range(getYearsSincePurchase(date_val)):
        fee += percentage_fees * invested_amount
    return fee


def addPost2019Fees(date_val: datetime, invested_amount: int, percentage_fees: int):
    fee: float = 0

    # initial fee
    fee += getDayOfYearPercentage(date_val) * invested_amount * percentage_fees

    for year in range(getYearsSincePurchase(date_val)):
        if year == 0:
            fee += percentage_fees * invested_amount
        elif year == 1:
            fee += (percentage_fees - POINT_TWO_PERCENT) * invested_amount
        elif year == 2:
            fee += (percentage_fees - POINT_FIVE_PERCENT) * invested_amount
        else:
            fee += (percentage_fees - ONE_PERCENT) * invested_amount

        fee += percentage_fees * invested_amount
    return fee


class Investor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    credit = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"Investor {self.id} - {self.name}"


class Investment(models.Model):
    id = models.AutoField(primary_key=True)
    investor_id = models.ForeignKey(Investor, on_delete=models.CASCADE)
    startup_name = models.CharField(max_length=100)
    invested_amount = models.DecimalField(max_digits=12, decimal_places=0)
    percentage_fees = models.DecimalField(max_digits=2, decimal_places=0)
    date_added = models.DateTimeField()
    fees_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES)

    def __str__(self):
        return f"Investment {self.id} - {self.startup_name}"

    def generate_bill(self):
        fee = 0
        if self.invested_amount < LARGE_INVESTMENT_THRESHOLD:
            fee += getYearsSincePurchase(self.date_added) * MEMBERSHIP_FEE
            print("membership fee added")

        if self.fee_type == "upfront":
            fee += (
                self.invested_amount
                * self.percentage_fees
                * getYearsSincePurchase(self.date_added)
            )
            print("upfront fee added")
        else:
            if self.date_added < FEE_UPDATE_DATE:
                fee += addPre2019Fees(
                    self.date_added, self.invested_amount, self.percentage_fees
                )
                print("Pre 2019 fee added")
            else:
                fee += addPost2019Fees(
                    self.date_added, self.invested_amount, self.percentage_fees
                )
                print("Post 2019 fee added")
        return fee


class Bill(models.Model):

    id = models.AutoField(primary_key=True)
    investor_id = models.ForeignKey(Investor, on_delete=models.CASCADE)
    investment_id = models.ForeignKey(Investment, on_delete=models.CASCADE)
    fees_amount = models.DecimalField(max_digits=12, decimal_places=0)
    date_added = models.DateTimeField()
    fees_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES)

    def __str__(self):
        return f"Bill {self.id} - {self.fees_amount}"


class CashCall(models.Model):
    id = models.AutoField(primary_key=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=0)
    IBAN = models.CharField(max_length=100)
    email_send = models.EmailField()
    date_added = models.DateTimeField()
    invoice_status = models.CharField(
        max_length=20, choices=INVOICE_STATUS_CHOICES, default="Pending"
    )

    def __str__(self):
        return f"CashCall {self.id} - {self.total_amount}"
