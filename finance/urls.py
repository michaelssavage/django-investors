from django.urls import path

from . import views

app_name = "finance"
urlpatterns = [
    path("", views.index, name="index"),
    path("investment/", views.investments, name="investments"),
    path("investment/<int:investment_id>/", views.investment, name="investment"),
    path("investor/", views.investors, name="investors"),
    path("investor/<int:investor_id>/", views.investor, name="investor"),
    path("bill/", views.bills, name="bills"),
    path("bill/<int:bill_id>/", views.bill, name="bill"),
    path("cashcall/<int:cashcall_id>/", views.cashcall, name="cashcall"),
    path("cashcall/", views.cashcalls, name="cashcalls"),
    path(
        "generate_investment_bill/<int:investment_id>/",
        views.generate_investment_bill,
        name="generate_investment_bill",
    ),
    path(
        "generate_investor_cash_call/<int:investor_id>/",
        views.generate_investor_cash_call,
        name="generate_investor_cash_call",
    ),
    path("generate_all_bills/", views.generate_all_bills, name="generate_all_bills"),
    path(
        "generate_all_cash_calls/",
        views.generate_all_cash_calls,
        name="generate_all_cash_calls",
    ),
    path(
        "update_invoice_status/<int:cashcall_id>/",
        views.update_invoice_status,
        name="update_invoice_status",
    ),
    path("send_invoice/<int:cashcall_id>/", views.send_invoice, name="send_invoice"),
]
