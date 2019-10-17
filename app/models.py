from django.db import models
import datetime

class Applicant(models.Model):

    APPROVAL_CHOICES = [
    (u'1', u'Awaiting'),
    (u'2', u'No'),
    (u'3', u'Yes')
    ]

    applicant_name = models.CharField(default=None, max_length=15)
    phone_number = models.IntegerField(default=None)
    d_o_b          = models.DateField(default=None)
    propel_mode    = models.CharField( default=None, max_length=15)
    job_state      = models.BooleanField(default=True)
    fcc_link       = models.CharField(default=None, max_length=150)
    interest       = models.CharField(default=None, max_length=250)
    fcc_eligible   = models.BooleanField(default=False)
    approval       = models.CharField(max_length=1, choices=APPROVAL_CHOICES, null=True)

class BatchDetail(models.Model):
    batch_type = models.CharField(null=True, max_length=30)
    date_from = models.DateField(default=datetime.date.today())
    to_date = models.DateField(default=None)
    strength = models.PositiveIntegerField(default=0, null=False)
    mentor_name = models.CharField(null=True, max_length=30)