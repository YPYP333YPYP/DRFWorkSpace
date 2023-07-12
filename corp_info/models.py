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


class Recruitment(models.Model):
    code = models.CharField(max_length=100)
    wantedAuthNo = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    salTpNm = models.CharField(max_length=255)
    sal = models.CharField(max_length=255)
    minSal = models.CharField(max_length=255)
    maxSal = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    holidayTpNm = models.CharField(max_length=255)
    minEdubg = models.CharField(max_length=255)
    career = models.CharField(max_length=255)
    regDt = models.CharField(max_length=255)
    closeDt = models.CharField(max_length=255)
    infoSvc = models.CharField(max_length=255)
    wantedInfoUrl = models.CharField(max_length=255)
    wantedMobileInfoUrl = models.CharField(max_length=255)
    smodifyDtm = models.CharField(max_length=255)
    zipCd = models.CharField(max_length=255)
    strtnmCd = models.CharField(max_length=255)
    basicAddr = models.CharField(max_length=255)
    empTpCd = models.IntegerField()
    jobsCd = models.IntegerField()

