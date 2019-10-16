from django.db import models

# Create your models here.

class Snippet(models.Model):
    name = models.CharField(max_length=15)
    phone_no = models.IntegerField()


    def __str__(self):
        return self.name


class Applicant(models.Model):
    name = models.CharField(max_length=15)
    #phone_no = models.IntegerField()


    def __str__(self):
        return self.name