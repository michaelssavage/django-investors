from datetime import datetime, timezone
from decimal import Decimal
from django.test import TestCase
from freezegun import freeze_time

from finance.models import Investment, Investor
from finance.utils import get_day_of_year_percentage, get_remaining_years_since_purchase


@freeze_time("2024-04-03 12:12:12.123456+00:00")
class FeesTestCase(TestCase):
    def setUp(self):
        self.default_investor = Investor.objects.create(
            name="Segismundo Marquez Casas",
            address="Via Jose Angel",
            credit="1234-5678-1234-5678",
            phone="123456789",
            email="segismundo_marquez_casas@fakeemail.com",
        )

        self.investment = Investment.objects.create(
            investor_id=self.default_investor,
            startup_name="startup",
            invested_amount=81000,
            percentage_fees=15,
            date_added=self.createUtcTime("2020-01-01 16:38:21"),
            fees_type="Yearly",
        )

        self.simple_investment = Investment.objects.create(
            investor_id=self.default_investor,
            startup_name="startup",
            invested_amount=5,
            percentage_fees=10,
            date_added=self.createUtcTime("2022-03-13 12:12:12"),
            fees_type="Upfront",
        )

    def createUtcTime(self, string_time: str):
        time = datetime.strptime(string_time, "%Y-%m-%d %H:%M:%S")
        return time.replace(tzinfo=timezone.utc)

    def test_getRemainingYearsSincePurchase_expectSevenYears(self):
        eight_years_ago = self.createUtcTime("2016-01-01 12:12:12")
        result = get_remaining_years_since_purchase(eight_years_ago)
        self.assertEqual(result, 7)

    def test_getRemainingYearsSincePurchase_expectZeroYears(self):
        one_day_ago = self.createUtcTime("2024-04-03 12:12:12")
        result = get_remaining_years_since_purchase(one_day_ago)
        self.assertEqual(result, 0)

    def test_getRemainingYearsSincePurchase_expectThreeYears(
        self,
    ):
        result = get_remaining_years_since_purchase(self.investment.date_added)
        self.assertEqual(result, 3)

    def test_getDayOfYearPercentage_expectFirstDayOfYear(self):
        first_of_january = self.createUtcTime("2016-01-01 12:12:12")
        result = get_day_of_year_percentage(first_of_january)
        # 1/365 = 0.0027 = 0.003
        self.assertEqual(result, Decimal(str(0.003)))

    def test_getDayOfYearPercentage_expectLastDayOfYear(self):
        new_years_eve = self.createUtcTime("2016-12-31 12:12:12")
        result = get_day_of_year_percentage(new_years_eve)
        # 365/365 = 1
        self.assertEqual(result, Decimal(1))

    def test_addPre2019Fees_usingOneYear(self):
        result = self.simple_investment.add_pre_2019_fees()
        # 13 march = 73rd day/365 = 0.197 = 0.2
        # initial fee = 73rd day / 365 * 5 * 0.1 = 10c
        # 1 year = 0.1 * 5 = 50c
        self.assertEqual(result, Decimal(str(0.5985)))

    def test_addPre2019Fees_usingThreeYears(self):
        result = self.investment.add_pre_2019_fees()
        # initial fee = 1/365 * €81,000 * 0.15 = €36.45
        # rest of fees = €81,000 * 0.15 * 3 = €36450
        self.assertEqual(result, Decimal(str(36486.45000)))

    def test_addPost2019Fees_usingOneYear(self):
        result = self.simple_investment.add_post_2019_fees()
        self.assertEqual(result, Decimal(str(0.5985)))

    def test_addPost2019Fees_usingThreeYears(self):
        result = self.investment.add_post_2019_fees()
        # initial fee = 1/365 * €81,000 * 0.15 = €36.45
        # year 1 = €81,000 * 0.15 = €12150
        # year 2 = €81,000 * 0.15 - 0.02 = €10530
        # year 3 = €81,000 * 0.15 - .05 = €8,100
        self.assertEqual(result, Decimal(str(35919.45000)))

    def test_add_membershipFees_forEveryYear(self):
        result = self.simple_investment.add_membership_fee()
        self.assertEqual(result, Decimal(3000))

    def test_dontAddMembershipFees_ifMoreThanThreshold(self):
        result = self.investment.add_membership_fee()
        self.assertEqual(result, 0)

    def test_addUpfrontFees_usingOneYear(self):
        result = self.simple_investment.add_upfront_fee()
        self.assertEqual(result, Decimal(str(2.5)))

    def test_generateBill_membership_upfront(self):
        result = self.simple_investment.generate_bill()
        # add membership (3000) + upfront costs (2.5)
        self.assertEqual(result, Decimal(str(3002.5)))

    def test_generateBill_yearly(self):
        result = self.investment.generate_bill()
        # add post 2019 fees only
        self.assertEqual(result, Decimal(str(35919.45000)))
