from django.shortcuts import get_object_or_404, render
from finance.models import Investment, Investor


def index(request):
    investments = Investment.objects.order_by("-id")
    investors = Investor.objects.order_by("-id")
    context = {"investments": investments, "investors": investors}
    return render(request, "finance/index.html", context)


def investment(request, investment_id):
    investment = get_object_or_404(Investment, pk=investment_id)
    return render(request, "finance/investment.html", {"investment": investment})


def investor(request, investor_id):
    investor = get_object_or_404(Investor, pk=investor_id)
    return render(request, "finance/investor.html", {"investor": investor})


def generate_bill(request, investment_id):
    if request.method == "POST":
        # Assuming Investment object is retrieved based on some criteria
        investment = Investment.objects.get(pk=investment_id)
        fee = investment.generate_bill()  # Call generate_bill function
        print(fee)
    return render(
        request, "finance/investment.html", {"investment": investment, "fee": fee}
    )
