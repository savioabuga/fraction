from smartmin.views import SmartCRUDL, SmartListView, SmartCsvView
from .models import Transaction


class TransactionCRUDL(SmartCRUDL):
    permissions = False
    model = Transaction
    actions = ("read", "update", "list", "csv")

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
            "date"
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