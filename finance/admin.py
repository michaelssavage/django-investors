from django.contrib import admin
from .models import Investor, Investment, Bill, CashCall

admin.site.register(Investor)
admin.site.register(Investment)
admin.site.register(Bill)
admin.site.register(CashCall)
