from __future__ import absolute_import, unicode_literals
from django.conf import settings
from django.contrib import admin
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from .models import Applicant, BatchDetail
from propel_school.celery import app
import requests
import json
from time import sleep

class ApplicantAdmin(admin.ModelAdmin):
    model = Applicant
    list_display = ('applicant_name', 'applicant_id', 'phone_number', 'approval','points')
    list_filter = ('applicant_name', 'approval',)
    search_fields = ('applicant_id__email','applicant_id__full_name')
    actions = ('fetch_fcc_points', 'private_profile', 'not_enough_points', 'wrong_link', 'shortlist_condidate', \
        'join_propel', 'propel_challenge', 'Extended_propel_challenge')

    def private_profile(self, request, queryset):
        queryset.update(approval='2')

    def not_enough_points(self, request, queryset):
        queryset.update(approval='3')

    def wrong_link(self, request, queryset):
        queryset.update(approval='4')

    def shortlist_condidate(self, request, queryset):
        queryset.update(approval='5')
        subject = 'Propel School | Confirmation for program starting 7th Jan, 2019'
        text_content = render_to_string('app/shortlist_email.txt')
        html_content = render_to_string('app/shortlist_email.html')
        for email in queryset:
            to = str(email.applicant_id)
            email_by_admin(subject, text_content, to, html_content)


    def join_propel(self, request, queryset):
        queryset.update(approval='6')

    def propel_challenge(self, request, queryset):
        queryset.update(approval='7')
        subject = "Propel School | Challenge"
        text_content = render_to_string('app/propel_challenge_email.txt')
        html_content = render_to_string('app/propel_challenge_email.html')
        for email in queryset:
            to = str(email.applicant_id)
            email_by_admin(subject, text_content, to, html_content)

    def Extended_propel_challenge(self, request, queryset):
        queryset.update(approval='8')
        subject = "Extended Propel Challenge"
        text_content = render_to_string('app/extended_propel_challenge_email.txt')
        html_content = render_to_string('app/extended_propel_challenge_email.html')
        for email in queryset:
            to = str(email.applicant_id)
            email_by_admin(subject, text_content, to, html_content)

    def fetch_fcc_points(self, request, queryset):
        for data in queryset:
            # celery_id= fetch_score.delay(data.fcc_link)
            # sleep(1)
            # data.points = celery_id.get()
            # print(celery_id.get())
            data.points = fetch_score(str(data.fcc_link))
            print('Hello')
            data.save()


#Function to send email
def email_by_admin(subject, text_content, to, html_content):
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, text_content, from_email, [to], html_message=html_content)


class BatchDetailAdmin(admin.ModelAdmin):
    list_display = ('batch_type', 'date_from', 'to_date', 'strength', 'mentor_name')
    search_fields = ('batch_type', 'date_from', 'to_date', 'mentor_name')


# Register your models here.
admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(BatchDetail, BatchDetailAdmin)


#function for fetching data from url
# @app.task(bind=True)
def fetch_score(url):
    profile = ""
    score = ""
    if url.find('freecodecamp.org') > 0:
      n = url.rfind('/')
      profile = url[n+1:len(url)]

    api = 'https://api.freecodecamp.org/internal/api/users/get-public-profile?username=' + profile

    try:
        response = requests.get(api)
        response = response.json()
        profile = next(iter(response['entities']['user']))
        if response['entities']['user'][profile]['profileUI']['isLocked']:
            return 'Private Profile'
        else:
            points = response['entities']['user'][profile]['points']
            score += str(points)
    except:
    	return 'Wrong Link'

    return score
