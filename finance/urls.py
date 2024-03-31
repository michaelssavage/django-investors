from django.urls import path

from . import views

app_name = "finance"
urlpatterns = [
    path("", views.index, name="index"),
    path("investment/<int:investment_id>/", views.investment, name="investment"),
    path("investor/<int:investor_id>/", views.investor, name="investor"),
    path("bill/<int:bill_id>/", views.bill, name="bill"),
    path("cashcall/<int:cashcall_id>/", views.cashcall, name="cashcall"),
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
]
