from django.contrib import admin
from .models import Applicant, BatchDetail

class BatchDetailAdmin(admin.ModelAdmin):
    list_display = ('batch_type', 'date_from', 'to_date', 'strength', 'mentor_name')
    search_fields = ('batch_type', 'date_from', 'to_date', 'mentor_name')


# Register your models here.
admin.site.register(Applicant)
admin.site.register(BatchDetail, BatchDetailAdmin)
