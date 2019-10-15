from django import forms

class ApplicationForm(forms.Form):
    applicant_name = forms.CharField()
    email = forms.EmailField(label="E-mail")
    phone_number = forms.IntegerField( widget=forms.TextInput(attrs={ 'max_length': 10, 'required': True, } ), )
