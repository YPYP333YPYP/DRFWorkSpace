from django.db import models


class Corporation(models.Model):
    corp_name = models.CharField(max_length=100)
    ceo_name = models.CharField(max_length=100)
    corp_addr = models.CharField(max_length=100)
    corp_homepage = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    est_date = models.CharField(max_length=100)
    sales_revenue = models.CharField(max_length=100)
    operating_profit = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.corp_name}'

class Technology(models.Model):
    tech_name = models.CharField(max_length=100)
    description = models.CharField(max_length=10000)

    def __str__(self):
        return self.tech_name


class SmartLogistics(models.Model):
    port_name = models.CharField(max_length=100)
    technology = models.ForeignKey(Technology, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.port_name



