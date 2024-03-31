from django.contrib import messages
from django.http import HttpResponseRedirect

BILL_EXISTS_WARNING = "A bill already exists for this investor and investment."
CASH_CALL_EXISTS_WARNING = "A cash call already exists for this investor."
BILL_SUCCESS = "Bill created successfully."
CASH_CALL_SUCCESS = "Cash Call created successfully."


def handle_redirect(redirect_url):
    return HttpResponseRedirect(redirect_url)
