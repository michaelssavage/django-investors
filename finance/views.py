from datetime import datetime, UTC
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from finance.utils import *
from finance.models import Bill, CashCall, Investment, Investor
import re


def index(request):
    investments = Investment.objects.order_by("-id")
    investors = Investor.objects.order_by("-id")
    bills = Bill.objects.order_by("-id")
    cashcalls = CashCall.objects.order_by("-id")
    context = {
        "investments": investments,
        "investors": investors,
        "bills": bills,
        "cashcalls": cashcalls,
    }
    return render(request, "finance/index.html", context)


def investment(request, investment_id):
    investment = get_object_or_404(Investment, pk=investment_id)
    investor = investment.investor_id
    context = {"investment": investment, "investor": investor}
    return render(request, "finance/investment.html", context)


def investor(request, investor_id):
    investor = get_object_or_404(Investor, pk=investor_id)
    return render(request, "finance/investor.html", {"investor": investor})


def bill(request, bill_id):
    bill = get_object_or_404(Bill, pk=bill_id)
    investor = bill.investor_id
    investment = bill.investment_id
    context = {"bill": bill, "investment": investment, "investor": investor}
    return render(request, "finance/bill.html", context)


def cashcall(request, cashcall_id):
    cashcall = get_object_or_404(CashCall, pk=cashcall_id)
    context = {"cashcall": cashcall}
    return render(request, "finance/cashcall.html", context)


def generate_all_bills(request):
    investments = Investment.objects.all()
    for investment in investments:
        generate_investment_bill(request, investment.id)
    return handle_redirect(reverse("finance:index"))


def generate_investment_bill(request, investment_id):
    investment = get_object_or_404(Investment, pk=investment_id)
    redirect_uri = reverse("finance:investment", args=(investment.id,))

    existing_bill = Bill.objects.filter(
        investor_id=investment.investor_id, investment_id=investment
    ).exists()
    if existing_bill:
        messages.warning(request, BILL_EXISTS_WARNING)
        return handle_redirect(redirect_uri)

    fee = investment.generate_bill()
    now = datetime.now(UTC)

    Bill.objects.create(
        investor_id=investment.investor_id,
        investment_id=investment,
        fees_amount=fee,
        date_added=now,
        fees_type=investment.fees_type,
    )
    messages.success(request, BILL_SUCCESS)
    return handle_redirect(redirect_uri)


def generate_all_cash_calls(request):
    investors = Investor.objects.all()
    for investor in investors:
        generate_investor_cash_call(request, investor.id)
    return handle_redirect(reverse("finance:index"))


def generate_investor_cash_call(request, investor_id):
    investor = get_object_or_404(Investor, pk=investor_id)
    redirect_uri = reverse("finance:investor", args=(investor.id,))

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
        messages.warning(request, CASH_CALL_EXISTS_WARNING)
        return handle_redirect(redirect_uri)

    CashCall.objects.create(
        total_amount=total_amount,
        IBAN=iban,
        email_send=investor.email,
        date_added=now,
        invoice_status="PENDING",
    )

    messages.success(request, CASH_CALL_SUCCESS)
    return handle_redirect(redirect_uri)
