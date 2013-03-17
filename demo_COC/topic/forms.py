# -*- coding: UTF-8 -*-
from django import forms



class NewTopicForm(forms.Form):
    title = forms.CharField(label=u'标题',min_length=4,required=True)
    content = forms.CharField(label=u'内容', widget=forms.Textarea,required=True)

        
        
        

