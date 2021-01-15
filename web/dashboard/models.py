from django.db import models
from djchoices import DjangoChoices, ChoiceItem


class Transaction(models.Model):
    class DepartmentType(DjangoChoices):
        government = ChoiceItem("government", "Government")
        midmarket = ChoiceItem("midmarket", "Midmarket")
        channel_partners = ChoiceItem("channel_partners", "Channel Partners")
        enterprise = ChoiceItem("enterprise", "Enterprise")

    class CountryChoice(DjangoChoices):
        canada = ChoiceItem("canada", "Canada")
        germany = ChoiceItem("germany", "Germany")
        mexico = ChoiceItem("mexico", "Mexico")
        usa = ChoiceItem("united_states_of_america", "United States of America")
        france = ChoiceItem("france", "France")

    class ProductType(DjangoChoices):
        carretera = ChoiceItem("carretera", "Carretera")
        paseo = ChoiceItem("paseo", "Paseo")
        velo = ChoiceItem("velo", "Velo")
        vtt = ChoiceItem("vtt", "VTT")
        montana = ChoiceItem("montana", "Montana")
        amarilla = ChoiceItem("amarilla", "Amarilla")

    class DiscoundBandType(DjangoChoices):
        low = ChoiceItem("low", "Low")
        medium = ChoiceItem("medium", "Medium")
        high = ChoiceItem("high", "High")

    department = models.CharField(max_length=100, choices=DepartmentType.choices)
    country = models.CharField(max_length=200, choices=CountryChoice.choices)
    product = models.CharField(max_length=100, choices=ProductType.choices)
    discount_band = models.CharField(max_length=100, blank=True)
    units_sold = models.DecimalField(max_digits=100, decimal_places=2)
    manufacturing_price = models.DecimalField(max_digits=20, decimal_places=2)
    sale_price = models.DecimalField(max_digits=20, decimal_places=2)
    gross_sales = models.DecimalField(max_digits=20, decimal_places=2)
    discounts = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    sales = models.DecimalField(max_digits=20, decimal_places=2)
    cogs = models.DecimalField(max_digits=20, decimal_places=2)
    profit = models.DecimalField(max_digits=20, decimal_places=2)
    date = models.DateField()
    month_number = models.IntegerField()
    month_name = models.CharField(max_length=20)
    year = models.IntegerField()