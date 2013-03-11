# -*- coding: UTF-8 -*-
from django import forms
from django.forms.util import ErrorList
from django.http import HttpRequest
from accounts.models import Student


class AccountsSignupForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
    realname = forms.CharField()
    
    gender = forms.CharField()

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            Student.objects.get(email=email)
        except Student.DoesNotExist:
            return email
        raise forms.ValidationError("此邮箱已经注册")
    
        
     
class AccountsLoginForm(forms.Form):
    login_email = forms.EmailField(max_length=128, label=u'电子邮件')
    login_password = forms.CharField(min_length=6,label=u'密码')
    remember_me = forms.CharField(required=False)
    
    def clean_email(self):
        email = self.cleaned_data['login_email']
        try:
            Student.objects.get(email=email)
        except Student.DoesNotExist:
            raise forms.ValidationError("邮箱不存在！")
        return email
    
    def clean_password(self):
        email = self.cleaned_data['login_email']
        password = self.cleaned_data['login_password']
        try:
            Student.objects.get(email=email,password=password)
        except Student.DoesNotExist:
            raise forms.ValidationError("邮箱和密码不匹配！")
        return password
    
    

class AccountsModifyProfileForm(forms.Form):
    
    realname = forms.CharField(label=u'真实姓名',max_length=5,min_length=1)
    
    
    face = forms.ImageField(label=u'头像', required=False)
    
    school = forms.CharField(label=u'学校', required=False)
    
    birthday = forms.DateField(label=u'生日')
    
class NewFeedForm(forms.Form):
    content = forms.CharField(required=False,widget=forms.Textarea)
    

     
class AccountsModifyPasswordForm(forms.Form):       
    pass

