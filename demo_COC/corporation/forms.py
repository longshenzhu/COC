# -*- coding: UTF-8 -*-
from django import forms

class CreatCorporationForm(forms.Form):
    name = forms.CharField()
    introduction = forms.CharField()
    birthyear = forms.IntegerField()
    school = forms.CharField()
    
    
    
    
    
    
class ModifyCorporationForm(forms.Form):
    name = forms.CharField()
    introduction = forms.CharField()