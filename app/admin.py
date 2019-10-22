from __future__ import absolute_import, unicode_literals
from django.conf import settings
from django.contrib import admin
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from .models import Applicant, BatchDetail, JoinedCandidate, Attendance, TaskList, TaskPerformance
from propel_school.celery import app
import requests
import json
from celery import shared_task
from time import sleep

#Admin class for Applicant model
class ApplicantAdmin(admin.ModelAdmin):
    model = Applicant
    list_display = ('applicant_name', 'applicant_id', 'phone_number', 'approval','points','join_confirm')
    list_filter = ('applicant_name', 'approval','join_confirm')
    search_fields = ('applicant_id__email','applicant_id__full_name')
    actions = ('fetch_fcc_points', 'shortlist_condidate', \
        'join_propel', 'propel_challenge', 'Extended_propel_challenge')

    # def private_profile(self, request, queryset):
    #     queryset.update(approval='2')

    # def not_enough_points(self, request, queryset):
    #     queryset.update(approval='3')

    # def wrong_link(self, request, queryset):
    #     queryset.update(approval='4')

    def shortlist_condidate(self, request, queryset):
        queryset.update(approval='5')
        subject = 'Propel School | Confirmation for program starting 7th Jan, 2019'
        text_content = render_to_string('app/shortlist_email.txt')
        html_content = render_to_string('app/shortlist_email.html')
        for email in queryset:
            to = str(email.applicant_id)
            email_by_admin.delay(subject, text_content, to, html_content)

    def join_propel(self, request, queryset):
        queryset.update(approval='6')
        batch_detail = BatchDetail.objects.values('id','date_from').order_by('-id')
        # batch_detail = BatchDetail.objects.values('id','date_from').order_by('-date_from')
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
            email_by_admin.delay(subject, text_content, to, html_content)

    def Extended_propel_challenge(self, request, queryset):
        queryset.update(approval='8')
        subject = "Extended Propel Challenge"
        text_content = render_to_string('app/extended_propel_challenge_email.txt')
        html_content = render_to_string('app/extended_propel_challenge_email.html')
        for email in queryset:
            to = str(email.applicant_id)
            email_by_admin.delay(subject, text_content, to, html_content)

    def fetch_fcc_points(self, request, queryset):
        for data in queryset:
            celery_id= fetch_score.delay(data.fcc_link)
            sleep(1)
            data.points = celery_id.get()
            # print(celery_id.get())
            # data.points = fetch_score(str(data.fcc_link))
            # print('Hello')
            data.save()
            if data.points == 'Wrong Link':
                if data.approval is not '4':
                    data.approval = '4'
                    data.save()
                    subject = 'Propel School | Please apply with correct FreeCodeCamp Profile'
                    text_content = render_to_string('app/wrong_link_email.txt')
                    html_content = render_to_string('app/wrong_link_email.html')
                    to = str(data.applicant_id)
                    email_by_admin.delay(subject, text_content, to, html_content)
                    print('wrong link')
            elif data.points == 'Private Profile':
                if data.approval is not '2':
                    data.approval = '2'
                    data.save()
                    subject = 'Propel School | Application Process - Make FCC Points Public'
                    text_content = render_to_string('app/private_profile_email.txt')
                    html_content = render_to_string('app/private_profile_email.html')
                    to = str(data.applicant_id)
                    email_by_admin.delay(subject, text_content, to, html_content)
                    print('private profile')
            elif int(data.points) <= 100:
                if data.approval is not '3':
                    data.approval = '3'
                    data.save()
                    subject = 'Propel School | Did not meet eligibility criteria'
                    text_content = render_to_string('app/not_eligible_email.txt')
                    html_content = render_to_string('app/not_eligible_email.html')
                    to = str(data.applicant_id)
                    email_by_admin.delay(subject, text_content, to, html_content)
            else:
                if data.approval is not '1':
                    data.approval = '1'
                    data.save()
                    subject = 'Propel School | Your application is waitlisted'
                    text_content = render_to_string('app/waitlist_email.txt')
                    html_content = render_to_string('app/waitlist_email.html')
                    to = str(data.applicant_id)
                    email_by_admin.delay(subject, text_content, to, html_content)

#Function to send email
@shared_task
def email_by_admin(subject, text_content, to, html_content):
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, text_content, from_email, [to], html_message=html_content)
    return None

class BatchDetailAdmin(admin.ModelAdmin):
    model = BatchDetail
    list_display = ('batch_type', 'date_from', 'to_date', 'strength', 'mentor_name')
    list_filter = ('date_from', 'mentor_name', 'batch_type')
    search_fields = ('batch_type', 'date_from', 'to_date', 'mentor_name')

#Admin class for Joined Candidates model
class JoinedCandidateAdmin(admin.ModelAdmin):
    model = JoinedCandidate
    list_display = ('candidate_name', 'candidate_id', 'batch_id', 'joined_on', 'remarks')
    list_filter = ('batch_id', 'candidate_name', 'joined_on')
    search_fields = ('candidate_name',)
    actions = ('add_to_attendance_table', 'add_task')

    def add_to_attendance_table(self, request, queryset):
        for query in queryset:
            # batch = JoinedCandidate.objects.filter(batch_id=query.batch.id)
            batch_id = query.batch.id
            candidate_name = query.candidate_name
            attendance = Attendance(batch_id=batch_id, candidate_name=candidate_name)
            attendance.save()
    
    def add_task(self, request, queryset):
        task = TaskList.objects.values('id', 'description').order_by('-id')
        task_id = task[0]['id']
        task_description = task[0]['description']
        for query in queryset:
            joinedcandidate_detail = JoinedCandidate.objects.get(id=query.id)
            # print(joinedcandidate_detail['id'])
            candidate_name = query.candidate_name
            taskperformance = TaskPerformance(task_id=task_id, joinedcandidate=joinedcandidate_detail, task_description=task_description, candidate_name=candidate_name)
            taskperformance.save()

#Admin class for Attendance model
class AttendanceAdmin(admin.ModelAdmin):
    model = Attendance
    list_display = ('candidate_name', 'batch_id', 'date', 'present', 'notes')
    list_filter = ('batch_id', 'candidate_name', 'date')
    search_fields = ('candidate_name', 'notes')
    actions = ('present', 'absent',)

    def present(self, request, queryset):
        queryset.update(present=True)

    def absent(self, request, queryset):
        queryset.update(present=False)

class TaskListAdmin(admin.ModelAdmin):
    model = TaskList
    list_display = ('description', 'id')
    list_filter = ('id', 'description')
    search_fields = ('description',)

class TaskPerformanceAdmin(admin.ModelAdmin):
    model = TaskPerformance
    list_display = ('task_description', 'task_id', 'joinedcandidate', 'candidate_name', 'notes')
    list_filter = ('task_id', 'candidate_name', 'task_description')
    search_fields = ('candidate_name','task_description')

# Register your models here.
admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(BatchDetail, BatchDetailAdmin)
admin.site.register(JoinedCandidate, JoinedCandidateAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(TaskList, TaskListAdmin)
admin.site.register(TaskPerformance, TaskPerformanceAdmin)

#function for fetching data from url
# @app.task(bind=True)
@shared_task
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

