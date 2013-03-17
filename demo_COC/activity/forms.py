# -*- coding: UTF-8 -*-
from django import forms

class CreatActivityForm(forms.Form):
    name = forms.CharField(required=True)