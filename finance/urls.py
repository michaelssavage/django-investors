from django.urls import path

from . import views

app_name = "finance"
urlpatterns = [
    path("", views.index, name="index"),
    path("investment/<int:investment_id>/", views.investment, name="investment"),
    path("investor/<int:investor_id>/", views.investor, name="investor"),
    path("bill/<int:bill_id>/", views.bill, name="bill"),
    path("cashcall/<int:cashcall_id>/", views.cashcall, name="cashcall"),
    path("<int:investor_id>/", views.generate_cash_call, name="generate_cash_call"),
    path("<int:investment_id>/", views.generate_bill, name="generate_bill"),
]
