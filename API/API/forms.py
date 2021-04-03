from django import forms
from django.forms import ModelForm
from .models import FTD, FTD_ElEMENTY


class FTDForm(forms.ModelForm):
    class Meta:
        model = FTD
        fields = ['nazwa', 'opis']


class FTD_ELEMENTYForm(forms.ModelForm):
    class Meta:
        model = FTD_ElEMENTY
        fields = ['id_ftd', 'id_dzl']
