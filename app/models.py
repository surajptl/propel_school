from django.db import models
from users.models import CustomUser
import datetime


class Applicant(models.Model):

    APPROVAL_CHOICES = [
    (u'1', u'Waitlist'),
    (u'2', u'Private'),
    (u'3', u'Not Enough Points'),
    (u'4', u'Wrong Link'),
    (u'5', u'Shortlist'),
    (u'6', u'Joined'),
    (u'7', u'Propel Challenge'),
    (u'8', u'Extended Propel Challenge'),
    ]

    applicant_id   = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, default=1)
    applicant_name = models.CharField(default=None, max_length=15)
    phone_number   = models.IntegerField(default=None)
    d_o_b          = models.DateField(default=None)
    propel_mode    = models.CharField( default=None, max_length=15)
    job_state      = models.BooleanField(default=True)
    fcc_link       = models.CharField(default=None, max_length=150)
    interest       = models.CharField(default=None, max_length=250)
    fcc_eligible   = models.BooleanField(default=False)
    points         = models.CharField(default="", null=True, max_length=10)
    join_confirm   = models.BooleanField(default=None, null = True)
    attended_propel_before   = models.BooleanField(default=None, null = True)
    approval       = models.CharField(default='1',max_length=1, choices=APPROVAL_CHOICES, null=True)
    join_confirm   = models.BooleanField(default=None, null=True)
    attended_propel_before = models.BooleanField(default=None, null=True)

class BatchDetail(models.Model):
    batch_type     = models.CharField(null=True, max_length=30)
    date_from      = models.DateField(default=datetime.date.today())
    to_date        = models.DateField(default=None)
    strength       = models.PositiveIntegerField(default=0, null=False)
    mentor_name    = models.CharField(null=True, max_length=30)

class JoinedCandidate(models.Model):
    batch = models.ForeignKey(BatchDetail, on_delete=models.CASCADE)
    candidate_id = models.OneToOneField(Applicant, on_delete=models.CASCADE)
    candidate_name = models.CharField(null=True, max_length=64)
    joined_on = models.DateField(default=None)
    remarks = models.CharField(null=True, max_length=150)

class Attendance(models.Model):
    # batch = models.ForeignKey(JoinedCandidate, on_delete=models.CASCADE)
    batch_id = models.IntegerField(null=True, default=1)
    candidate_name = models.CharField(null=True, max_length=64)
    date = models.DateField(default=datetime.date.today())
    present = models.BooleanField(default=False)
    notes = models.CharField(null=True, max_length=250)
