from django.views import View
from django.db.models import Sum
from django.shortcuts import render
from smartmin.views import SmartCRUDL, SmartListView, SmartCsvView, SmartView, SmartTemplateView
from chartit import PivotDataPool, PivotChart
from .models import Transaction


class TransactionCRUDL(SmartCRUDL):
    permissions = False
    model = Transaction
    actions = ("read", "update", "list", "csv", "chart")

    class List(SmartListView):
        fields = (
            "id",
            "department",
            "country",
            "product",
            "discount_band",
            "units_sold",
            "manufacturing_price",
            "sale_price",
            "gross_sales",
            "discounts",
            "sales",
            "cogs",
            "profit",
            "date",
        )

        def get_department(self, obj):
            return Transaction.DepartmentType.get_choice(obj.department).label

        def get_country(self, obj):
            return Transaction.CountryChoice.get_choice(obj.country).label

        def get_product(self, obj):
            return Transaction.ProductType.get_choice(obj.product).label

        def get_discount_band(self, obj):
            try:
                discount_band = Transaction.DiscoundBandType.get_choice(obj.discount_band).label
            except KeyError:
                discount_band = ""
            return discount_band

        def get_queryset(self, **kwargs):
            queryset = super().get_queryset(**kwargs)
            transaction_filter = self.request.GET.get("transaction_filter")
            department_choices = dict(Transaction.DepartmentType.choices).keys()
            product_choices = dict(Transaction.ProductType.choices).keys()
            if transaction_filter in department_choices:
                queryset = queryset.filter(department=transaction_filter)
            elif transaction_filter in product_choices:
                queryset = queryset.filter(product=transaction_filter)
            return queryset

    class Csv(SmartCsvView, List):
        pass

    class Chart(SmartTemplateView):
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            sales_datapool = PivotDataPool(
                series=[
                    {
                        "options": {
                            "source": Transaction.objects.all(),
                            "categories": ["product"],
                            "legend_by": "country",
                            "top_n_per_cat": 3,
                        },
                        "terms": {"sales": Sum("sales")},
                    }
                ]
            )

            sales_chart = PivotChart(
                datasource=sales_datapool,
                series_options=[{"options": {"type": "column", "stacking": True}, "terms": ["sales"]}],
                chart_options={
                    "title": {"text": "Sales by product in top 3 countries"},
                    "xAxis": {"title": {"text": "Product"}},
                },
            )

            profits_datapool = PivotDataPool(
                series=[
                    {
                        "options": {
                            "source": Transaction.objects.all(),
                            "categories": ["month_number"],
                            "legend_by": "product",
                            "top_n_per_cat": 5,
                        },
                        "terms": {"profit": Sum("profit")},
                    }
                    
                ],
                sortf_mapf_mts = (lambda *x: (1*x), None, None)
            )

            profit_chart = PivotChart(
                datasource=profits_datapool,
                series_options=[{"options": {"type": "column", "stacking": False}, "terms": ["profit"]}],
                chart_options={
                    "title": {"text": "Profit by Month in top 3 products"},
                    "xAxis": {"title": {"text": "Month"}},
                },
            )

            context["charts"] = [sales_chart, profit_chart]

            return context
