from django.contrib import admin
from .models import Applicant, BatchDetail

class ApplicantAdmin(admin.ModelAdmin):
    model = Applicant
    list_display = ('applicant_name', 'applicant_id', 'phone_number', 'approval',)
    list_filter = ('applicant_name', 'approval',)
    search_fields = ('applicant_id__email','applicant_id__full_name')


class BatchDetailAdmin(admin.ModelAdmin):
    list_display = ('batch_type', 'date_from', 'to_date', 'strength', 'mentor_name')
    search_fields = ('batch_type', 'date_from', 'to_date', 'mentor_name')


# Register your models here.
admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(BatchDetail, BatchDetailAdmin)
