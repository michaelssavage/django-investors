from datetime import UTC, datetime
from decimal import Decimal
from django.http import HttpResponseRedirect

BILL_EXISTS_WARNING = "A bill already exists for this investor and investment."
CASH_CALL_EXISTS_WARNING = "A cash call already exists for this investor."

PAYMENT_CHOICES = [
    ("Upfront", "Upfront"),
    ("Yearly", "Yearly"),
]

POINT_TWO_PERCENT = Decimal(str(0.002))
POINT_FIVE_PERCENT = Decimal(str(0.005))
ONE_PERCENT = Decimal(str(0.01))
FEE_UPDATE_DATE = datetime(2019, 4, 1).timestamp()
LARGE_INVESTMENT_THRESHOLD = Decimal(50000)
MEMBERSHIP_FEE = Decimal(3000)
UPFRONT_YEARS = Decimal(5)


def get_day_of_year_percentage(date_val: datetime):
    value = date_val.timetuple().tm_yday
    if value >= 365:
        return Decimal(1)
    else:
        # round to 3 decimal places
        return Decimal(str(round((value / 365), 3)))


def get_remaining_years_since_purchase(date_val: datetime):
    years = round((datetime.now(UTC) - date_val).days / 365) - 1
    if years < 0:
        return 0
    return years


def handle_redirect(redirect_url):
    return HttpResponseRedirect(redirect_url)
