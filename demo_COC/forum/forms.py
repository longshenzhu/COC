# -*- coding: UTF-8 -*-
from django import forms
from django.forms.util import ErrorList
from django.http import HttpRequest
from accounts.models import Student
from forum.models import Topic
from corporation.models import Corporation



class NewTopicForm(forms.Form):
    title = forms.CharField(label=u'标题')
    content = forms.CharField(label=u'内容', widget=forms.Textarea)

        
        
        
class NewPostForm(forms.Form):
    content = forms.CharField(label=u'回应', widget=forms.Textarea)
