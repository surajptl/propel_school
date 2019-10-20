from django.conf import settings
from django.contrib import admin
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from .models import Applicant, BatchDetail, JoinedCandidate
# import requests
import json

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
        batch_detail = BatchDetail.objects.values('id','date_from').order_by('-date_from')
        batch_id = batch_detail[0]['id']
        join_on = batch_detail[0]['date_from']
        for applicant in queryset:
            candidate_detail = Applicant.objects.get(applicant_id=applicant.applicant_id)
            # candidate_id = applicant.applicant_id
            candidate_name = applicant.applicant_name
            jc = JoinedCandidate(batch_id=batch_id, candidate_id=candidate_detail, candidate_name=candidate_name, joined_on=join_on)
            jc.save()

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
            data.points = fetch_score(data.fcc_link)
            data.save()

class BatchDetailAdmin(admin.ModelAdmin):
    model = BatchDetail
    list_display = ('batch_type', 'date_from', 'to_date', 'strength', 'mentor_name')
    list_filter = ('date_from', 'mentor_name', 'batch_type')
    search_fields = ('batch_type', 'date_from', 'to_date', 'mentor_name')
    
class JoinedCandidateAdmin(admin.ModelAdmin):
    model = JoinedCandidate
    list_display = ('batch_id', 'candidate_id', 'candidate_name', 'joined_on', 'remarks')
    list_filter = ('batch_id', 'candidate_name', 'joined_on')
    search_fields = ('candidate_name',)

# Register your models here.
admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(BatchDetail, BatchDetailAdmin)
admin.site.register(JoinedCandidate, JoinedCandidateAdmin)


#Function to send email
def email_by_admin(subject, text_content, to, html_content):
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, text_content, from_email, [to], html_message=html_content)


#function for fetching data from url
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
        if response['entities']['user'][profile]['profileUI']['isLocked']:
            return 'Private Profile'
        else:
            points = response['entities']['user'][profile]['points']
            score += str(points)
    except:
    	return 'Wrong Link'

    return score
