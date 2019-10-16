from django.db import models

# Create your models here.

# class Snippet(models.Model):
#     name = models.CharField(max_length=15)
#     phone_no = models.IntegerField()


#     def __str__(self):
#         return self.name


class Applicant(models.Model):
    applicant_name = models.CharField(default=None, max_length=15)
    phone_number = models.IntegerField(default=None)
    d_o_b          = models.DateField(default=None)
    propel_mode    = models.CharField( default=None, max_length=15)
    job_state      = models.BooleanField(default=True)
    fcc_link       = models.CharField(default=None, max_length=150)
    interest       = models.CharField(default=None, max_length=250)
    fcc_eligible   = models.BooleanField(default=False) 
