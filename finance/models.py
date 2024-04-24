from datetime import datetime, UTC
from decimal import Decimal
from django import forms
from django.db import models
from django.contrib.admin.helpers import ActionForm

from finance.utils import (
    PAYMENT_CHOICES,
    POINT_TWO_PERCENT,
    POINT_FIVE_PERCENT,
    ONE_PERCENT,
    FEE_UPDATE_DATE,
    LARGE_INVESTMENT_THRESHOLD,
    MEMBERSHIP_FEE,
    UPFRONT_YEARS,
    get_day_of_year_percentage,
    get_remaining_years_since_purchase,
)


class Investor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    credit = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Investment(models.Model):

    id = models.AutoField(primary_key=True)
    investor_id = models.ForeignKey(Investor, on_delete=models.CASCADE)
    startup_name = models.CharField(max_length=100)
    invested_amount = models.DecimalField(max_digits=12, decimal_places=0)
    percentage_fees = models.DecimalField(max_digits=2, decimal_places=0)
    date_added = models.DateTimeField()
    fees_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES)

    class Meta:
        ordering = ["id"]

    def save(self, *args, **kwargs):
        self.percentage_fees = Decimal(str(self.percentage_fees / 100))
        super().save(*args, **kwargs)

    def display_percentage_fees(self):
        return self.percentage_fees * 100

    def __str__(self):
        return self.startup_name

    def add_pre_2019_fees(self):
        fee: Decimal = 0

        # first year
        fee += (
            get_day_of_year_percentage(self.date_added)
            * self.invested_amount
            * self.percentage_fees
        )

        # other years
        for _ in range(get_remaining_years_since_purchase(self.date_added)):
            fee += self.percentage_fees * self.invested_amount

        return fee

    def add_post_2019_fees(self):
        fee: Decimal = 0

        # initial fee
        fee += (
            get_day_of_year_percentage(self.date_added)
            * self.invested_amount
            * self.percentage_fees
        )
        for index in range(get_remaining_years_since_purchase(self.date_added)):
            # year 1
            if index == 0:
                fee += self.percentage_fees * self.invested_amount
            # year 2
            elif index == 1:
                fee += (self.percentage_fees - POINT_TWO_PERCENT) * self.invested_amount
            # year 3
            elif index == 2:
                fee += (
                    self.percentage_fees - POINT_FIVE_PERCENT
                ) * self.invested_amount
            else:
                fee += (self.percentage_fees - ONE_PERCENT) * self.invested_amount

        return fee

    def add_membership_fee(self):
        fee = 0
        if self.invested_amount < LARGE_INVESTMENT_THRESHOLD:
            fee += get_remaining_years_since_purchase(self.date_added) * MEMBERSHIP_FEE
        return fee

    def add_upfront_fee(self):
        fee = 0
        fee += self.invested_amount * self.percentage_fees * UPFRONT_YEARS
        return fee

    def generate_bill(self):
        fee = 0
        fee += self.add_membership_fee()
        print(f"membership fee added: {fee}")

        if self.fees_type == "Upfront":
            fee += self.add_upfront_fee()
            print("upfront fee added")
        else:
            if self.date_added.timestamp() < FEE_UPDATE_DATE:
                fee += self.add_pre_2019_fees()
                print("Pre 2019 fee added")
            else:
                fee += self.add_post_2019_fees()
                print("Post 2019 fee added")
        return fee


class Bill(models.Model):

    id = models.AutoField(primary_key=True)
    investor_id = models.ForeignKey(Investor, on_delete=models.CASCADE)
    investment_id = models.ForeignKey(Investment, on_delete=models.CASCADE)
    fees_amount = models.DecimalField(max_digits=12, decimal_places=0)
    date_added = models.DateTimeField()
    fees_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"Bill {self.id}"


class CashCall(models.Model):
    INVOICE_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Validated", "Validated"),
        ("Sent", "Sent"),
        ("Paid", "Paid"),
        ("Overdue", "Overdue"),
    ]
    id = models.AutoField(primary_key=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=0)
    IBAN = models.CharField(max_length=100)
    email_send = models.EmailField()
    date_added = models.DateTimeField()
    invoice_status = models.CharField(
        max_length=20, choices=INVOICE_STATUS_CHOICES, default="Pending"
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"CashCall {self.id}"


class GroupBills(ActionForm):
    investor = forms.ModelChoiceField(queryset=Investor.objects.all(), required=False)


class GroupInvoiceStatus(ActionForm):
    invoice_status = forms.ChoiceField(
        choices=CashCall.INVOICE_STATUS_CHOICES, required=False
    )
