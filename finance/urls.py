from django.urls import path

from . import views

app_name = "finance"
urlpatterns = [
    path("", views.index, name="index"),
    path("investment/<int:investment_id>/", views.investment, name="investment"),
    path("investor/<int:investor_id>/", views.investor, name="investor"),
    path("bill/<int:bill_id>/", views.bill, name="bill"),
    path("<int:investment_id>/", views.generate_bill, name="generate_bill"),
]
