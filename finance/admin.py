from django.contrib import admin
from .models import GroupInvoiceStatus, Investor, Investment, Bill, CashCall, GroupBills
from django.utils.translation import ngettext
from django.contrib import messages


class BillAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "investor_id",
        "investment_id",
    )
    action_form = GroupBills
    actions = ["group_bills"]

    @admin.action(description="Group bills by Investor")
    def group_bills(self, request, queryset):

        investor = Investor.objects.get(id=request.POST["investor"])
        updated = queryset.update(investor_id=investor)
        self.message_user(
            request,
            ngettext(
                "%d bill was successfully grouped by investor.",
                "%d stories were successfully grouped by investor.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )


class InvestorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )


class InvestmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "investor_id",
        "startup_name",
    )


class CashCallAdmin(admin.ModelAdmin):
    list_display = ("id", "total_amount", "current_invoice_status")

    action_form = GroupInvoiceStatus
    actions = ["group_invoices"]

    @admin.action(description="Group invoices by status")
    def group_invoices(self, request, queryset):

        print("r", request.POST["invoice_status"])
        print("q", queryset)
        invoice_status = request.POST["invoice_status"]
        updated = queryset.update(invoice_status=invoice_status)
        self.message_user(
            request,
            ngettext(
                "%d cash call invoice status was successfully updated.",
                "%d cash call invoice statuses were successfully updated.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    def current_invoice_status(self, obj):
        return obj.invoice_status


admin.site.register(Investor, InvestorAdmin)
admin.site.register(Investment, InvestmentAdmin)
admin.site.register(Bill, BillAdmin)
admin.site.register(CashCall, CashCallAdmin)
