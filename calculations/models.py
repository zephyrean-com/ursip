from django.db import models


class Company(models.Model):
    name = models.CharField(unique=True, max_length=80)


class BaseMeasurement(models.Model):
    class Meta:
        abstract = True

    class DataOrigin(models.TextChoices):
        FACT = 'M', 'Fact'  # [m]easured
        FORECAST = 'P', 'Forecast'  # [p]redicted

    class Substance(models.TextChoices):
        OIL = 'O', 'Oil'
        LIQ = 'L', 'Liq'

    date = models.DateField()
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    data_origin = models.CharField(max_length=1, choices=DataOrigin.choices)
    substance = models.CharField(max_length=1, choices=Substance.choices)


class Data1(BaseMeasurement):
    value = models.IntegerField()


class Data2(BaseMeasurement):
    value = models.IntegerField()
