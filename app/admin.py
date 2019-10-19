from django.contrib import admin
from .models import Applicant, BatchDetail
import requests
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

    def join_propel(self, request, queryset):
        queryset.update(approval='6')

    def propel_challenge(self, request, queryset):
        queryset.update(approval='7')

    def Extended_propel_challenge(self, request, queryset):
        queryset.update(approval='8')

    def fetch_fcc_points(self, request, queryset):
        for data in queryset:
            print(fetch_score(data.fcc_link))
            data.points = fetch_score(data.fcc_link)
            data.save()

class BatchDetailAdmin(admin.ModelAdmin):
    list_display = ('batch_type', 'date_from', 'to_date', 'strength', 'mentor_name')
    search_fields = ('batch_type', 'date_from', 'to_date', 'mentor_name')


# Register your models here.
admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(BatchDetail, BatchDetailAdmin)


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
