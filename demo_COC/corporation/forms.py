# -*- coding: UTF-8 -*-
from django import forms

class CreatCorporationForm(forms.Form):
    name = forms.CharField()
    introduction = forms.CharField()  # 小组简介
    # tags = fields.ListField(fields.StringField())#小组标签
    # school = fields.StringField()
    
class ModifyCorporationForm(forms.Form):
    name = forms.CharField()
    introduction = forms.CharField()