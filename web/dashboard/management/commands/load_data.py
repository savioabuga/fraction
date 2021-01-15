import csv
import os
import re
from datetime import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from dashboard.models import Transaction


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(file_path, "data.csv"), "r") as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                department = Transaction.DepartmentType.get_choice(row["department"].strip().lower().replace(" ", "_"))
                country = Transaction.CountryChoice.get_choice(row["country"].strip().lower().replace(" ", "_"))
                product = Transaction.ProductType.get_choice(row["product"].strip().lower())
                try:
                    discount_band = Transaction.DiscoundBandType.get_choice(row["discount_band"].strip().lower())
                except KeyError:
                    discount_band = ""
                units_sold = Decimal(row["units_sold"])
                manufacturing_price = self.currency_to_numeric(row["manufacturing_price"])
                sale_price = self.currency_to_numeric(row["sale_price"].replace("-", "0"))
                gross_sales = self.currency_to_numeric(row["gross_sales"].replace("-", "0"))
                discounts = self.currency_to_numeric(row["discounts"].replace("-", "0"))
                sales = self.currency_to_numeric(row["sales"].replace("-", "0"))
                cogs = self.currency_to_numeric(row["cogs"].replace("-", "0"))
                profit = self.currency_to_numeric(row["profit"].replace("-", "0"))
                date = datetime.strptime(row["date"], "%m/%d/%Y")
                month_number = int(row["month_number"])
                month_name = row["month_name"].strip()
                year = int(row["year"])
                Transaction.objects.create(
                    department=department.value,
                    country=country.value,
                    product=product.value,
                    discount_band=discount_band,
                    units_sold=units_sold,
                    manufacturing_price=manufacturing_price,
                    sale_price=sale_price,
                    gross_sales=gross_sales,
                    discounts=discounts,
                    sales=sales,
                    cogs=cogs,
                    profit=profit,
                    date=date,
                    month_number=month_number,
                    month_name=month_name,
                    year=year
                )

    def currency_to_numeric(self, money):
        return Decimal(re.sub(r"[^\d.]", "", money))
