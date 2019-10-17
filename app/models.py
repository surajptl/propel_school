from django.db import models
from users import models as user_models
from users.models import CustomUser

class Applicant(models.Model):

    APPROVAL_CHOICES = [
    (u'1', u'Awaiting'),
    (u'2', u'No'),
    (u'3', u'Yes')
    ]

    applicant_id = models.OneToOneField(user_models.CustomUser, on_delete=models.CASCADE, primary_key=True, default=None)
    #applicant_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    applicant_name = models.CharField(default=None, max_length=15)
    phone_number = models.IntegerField(default=None)
    d_o_b          = models.DateField(default=None)
    propel_mode    = models.CharField( default=None, max_length=15)
    job_state      = models.BooleanField(default=True)
    fcc_link       = models.CharField(default=None, max_length=150)
    interest       = models.CharField(default=None, max_length=250)
    fcc_eligible   = models.BooleanField(default=False) 
    approval       = models.CharField(default='1',max_length=1, choices=APPROVAL_CHOICES, null=True)

    def __str__(self):
        return self.applicant_id.email
 