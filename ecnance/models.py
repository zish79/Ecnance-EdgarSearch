from django.db import models
from django import forms
# from msilib.MySQLdb import DATETIME
import datetime

# Create your models here.
class CIKPage(forms.Form):
    cik=forms.CharField(max_length=100)
    cname=forms.CharField(max_length=100)
    year=forms.ChoiceField(choices=[(x, x) for x in range(2005, 2014)])
    
class companies(models.Model):
    seq_id=models.IntegerField(primary_key=True)
    cik=models.CharField(max_length=50)
    company_name=models.CharField(max_length=2000)
    sic=models.CharField(max_length=200)
    
class ticker_data(models.Model):
    seq_id=models.IntegerField(primary_key=True)
    cik=models.CharField(max_length=50)
    xbrl=models.CharField(max_length=4294967295)
    year=models.CharField(max_length=4)
    execution_time=models.TimeField()
    
class ticker_data_new(models.Model):
    seq_id=models.IntegerField(primary_key=True)
    cik=models.CharField(max_length=50)
    keyratios=models.CharField(max_length=4294967295)
    xbrl_bs=models.CharField(max_length=4294967295)
    xbrl_is=models.CharField(max_length=4294967295)
    xbrl_cf=models.CharField(max_length=4294967295)
    xbrl_se=models.CharField(max_length=4294967295)
    year=models.CharField(max_length=4)
    execution_time=models.TimeField()
    chart_bs=models.CharField(max_length=4294967295)
    chart_is=models.CharField(max_length=4294967295)
    chart_cf=models.CharField(max_length=4294967295)
    chart_se=models.CharField(max_length=4294967295)