from django import forms
from .models import Dump


class ImportDataForm(forms.ModelForm):
    class Meta:
        model = Dump
        fields = ("org_name",)
#             "org_acronym",
#             "founding_year",
#             "years_active",
#             "org_type",
#             "org_legaltype",
#             "refugee_settlement",
#             "refugee_zone",
#             "org_offices",
#             "org_primarytechnicalarea",
#             "org_activities",
#             "org_secondarytechnicalarea1",
#             "org_secondarytechnicalarea2",
#             "org_targetgroup",
#             "org_targetdemographic",
#             "org_primarycontact",
#             "org_email",
#             "org_phone",
#             "org_website",
#             "org_facebook",
#             "org_twitter",
#             "org_logo",
#             "contact_name",
#             "contact_role",
#             "contact_email",
#             "contact_phone")
#



        # date_of_last_contact = forms.DateField(widget=forms.DateInput(
        #     attrs={
        #         'class': 'form-control',
        #         'placeholder': 'Username'
        #     }
        # ))
        # widgets = {
        #     'org_code': forms.TextInput(attrs={'class': 'form-control'}),
        #     'organisation_name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'website': forms.TextInput(attrs={'class': 'form-control'})
        # }


