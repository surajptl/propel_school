from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
from .models import Applicant
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

#add required fields

class ApplicationForm(forms.ModelForm):

    PROPEL_CHOICES = [
    ('online', 'Home (Online / Remote)'),
    ('campus', 'Propel School campus (J.P. Nagar Bangalore)'),
    ('open', 'Open to both online or at campus'),
    ]
    JOB_STATUS = [
        (True, 'Yes'),
        (False, 'No')
    ]
    FCC_STATUS = [
        (True, 'Yes'),
        (False, 'No'),
    ]
    
    applicant_name = forms.CharField(label='Name',max_length=15)
    phone_number   = forms.IntegerField( widget=forms.TextInput(attrs={ 'max_length': 10, 'required': True, } ), )
    #d_o_b          = forms.DateField(label="Date of Birth",widget=forms.SelectDateWidget())
    d_o_b = forms.DateTimeField(label="Date of Birth", input_formats=['%d/%m/%Y'], widget= forms.TextInput
    (attrs={'placeholder':'dd/mm/yyyy'}))
    propel_mode    = forms.CharField(label='Where would you like to attend the program from?', widget=forms.Select(choices=PROPEL_CHOICES))
    job_state      = forms.CharField(label='Are you actively looking for a job? ', widget=forms.Select(choices=JOB_STATUS))
    fcc_link       = forms.CharField(label='FreeCodeCamp Public Profile URL Link',max_length=50, widget= forms.TextInput
    (attrs={'placeholder':'you need a minimum of 100 points on freecodecamp to be eligible'}))
    interest       = forms.CharField(label='Why are you interested in this program?', widget=forms.Textarea)
    fcc_eligible   = forms.CharField(label='Do you have 100+ points in FreeCodeCamp?', widget=forms.Select(choices=FCC_STATUS))
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'applicant_name',
            'phone_number',
            'd_o_b',
            'propel_mode',
            'job_state',
            'fcc_eligible',
            'fcc_link',
            'interest',
            Submit('submit','Submit', css_class='btn-success')
        )


    class Meta:
        model = Applicant
        fields = ('applicant_name', 'phone_number', 'd_o_b', 'propel_mode', 'job_state','fcc_eligible',  'fcc_link', 'interest',)


# class SnippetForm(forms.ModelForm):

#     class Meta:
#         model = Snippet
#         fields = ('name', 'phone_no')