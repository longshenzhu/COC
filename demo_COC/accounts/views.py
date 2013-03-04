# -*- coding: UTF-8 -*-
import os
import datetime
from PIL import Image
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from demo_COC.settings import STATIC_URL, MEDIA_ROOT, MEDIA_URL
from models import Student, Public_Profile, S_S_Card, Feed, Event
from django.http import HttpResponseRedirect
from django.contrib.auth import *
from forms import AccountsSignupForm, AccountsLoginForm, AccountsModifyProfileForm, NewFeedForm
from django.template import RequestContext
from mongoengine.django.sessions import MongoSession
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

        

def indexsignup(request):
    form = AccountsSignupForm(request.POST)
    print form.is_valid()
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        realname = form.cleaned_data['realname']
        gender = form.cleaned_data['gender']
        student = Student.create_user(username=email, email=email, password=password)
        url_number = len(Student.objects)
        student.url_number = url_number
        public_profile = Public_Profile(realname=realname, gender=gender, face=STATIC_URL + 'img/face.png')
        
        student.public_profile = public_profile
        
        student.save()
        sscard = S_S_Card(user=student)
        sscard.save()
        event = Event(user=student)
        event.save()
        user = authenticate(username=email, password=password)
        request.session.set_expiry(0)
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render_to_response('404.html', {'STATIC_URL':STATIC_URL})
            
@login_required(login_url='/')            
def signup_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = AccountsModifyProfileForm(request.POST)
        if form.is_valid():
            realname = form.cleaned_data['realname']
            birthday = form.cleaned_data['birthday']
            public_profile = current_user.public_profile
            if request.FILES:
                path = 'img/student/' + str(current_user.url_number)
                if not os.path.exists(MEDIA_ROOT + path):
                    os.makedirs(MEDIA_ROOT + path)
                
                
                img = Image.open(request.FILES['face'])
                if img.mode == 'RGB':
                    filename = 'face.jpg'
                elif img.mode == 'P':
                    filename = 'face.png'
                filepath = '%s/%s' % (path, filename)
                # 获得图像的宽度和高度
                width, height = img.size
                # 计算高宽
                ratio = 1.0 * height / width
                # 计算新的高度
                new_height = int(260 * ratio)
                new_size = (260, new_height)
                # 缩放图像
                out = img.resize(new_size, Image.ANTIALIAS)
                out.save(MEDIA_ROOT + filepath)
                public_profile.face = MEDIA_URL + filepath
                
            public_profile.realname = realname
            public_profile.birthday = birthday
            current_user.public_profile = public_profile
            current_user.save()
            return HttpResponseRedirect('/')
    
    else:
        form = AccountsModifyProfileForm()
        return render_to_response('accounts/modifyprofile.html', {'form': form, 'STATIC_URL':STATIC_URL, 'current_user':current_user}, context_instance=RequestContext(request))
            

def indexlogin(request):
    form = AccountsLoginForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['login_email']
        password = form.cleaned_data['login_password']
        is_remember = form.cleaned_data['remember_me']
        if is_remember != 'remember':
            request.session.set_expiry(0)
        student = authenticate(username=email, password=password)
        if student is not None and student.is_active:
            login(request, student)
            return HttpResponseRedirect('/')
        else:
            return render_to_response('404.html', {'STATIC_URL':STATIC_URL})
            
    



def index(request):
    if request.session.session_key:
        current_user = request.user
        if current_user.is_authenticated():
            if request.method == 'POST':
                form = NewFeedForm(request.POST)
                if form.is_valid():
                    content = form.cleaned_data['content']
                    feed = Feed(content=content)
                    feed.creat_time = datetime.datetime.now()
                    current_user.update(push__feeds=feed)
                    return HttpResponseRedirect('/')
                    
            else:
                form = NewFeedForm()
                return render_to_response('accounts/broadcast.html', {'form':form, 'current_user':current_user, 'STATIC_URL':STATIC_URL}, context_instance=RequestContext(request))
        # 这里应该还有个else，来处理有sessiondata但是已经注销了的情况
        else:
            if request.method == 'POST':
                if 'login' in request.POST:
                    return indexlogin(request)
                elif 'signup' in request.POST:
                    return indexsignup(request)
            
            else:
                form_login = AccountsLoginForm()
                form_signup = AccountsSignupForm()
                return render_to_response('index.html', {'form_login': form_login, 'form_signup':form_signup, 'STATIC_URL':STATIC_URL}, context_instance=RequestContext(request))
                    
    else:
        if request.method == 'POST':
            if 'login' in request.POST:
                return indexlogin(request)
            elif 'signup' in request.POST:
                print 'signup'
                return indexsignup(request)

        else:
            form_login = AccountsLoginForm()
            form_signup = AccountsSignupForm()
            return render_to_response('index.html', {'form_login': form_login, 'form_signup':form_signup, 'STATIC_URL':STATIC_URL}, context_instance=RequestContext(request))

    
@login_required(login_url='/') 
def profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = AccountsModifyProfileForm(request.POST)
        if form.is_valid():
            realname = form.cleaned_data['realname']
            gender = form.cleaned_data['gender']
            school = form.cleaned_data['school']
            birthday = form.cleaned_data['birthday']
            face = form.cleaned_data['face']
            
            
    else:
        form = AccountsModifyProfileForm()
    return render_to_response('accounts/profile.html', {'form':form, 'STATIC_URL':STATIC_URL}, context_instance=RequestContext(request))
            


@login_required(login_url='/') 
def userlogout(request):
    logout(request)
    return HttpResponseRedirect('../')
            
    
def modifypassword(request):
    pass

@login_required(login_url='/')
def visit_people_feeds(request, url_number):
    student = Student.objects(url_number=url_number).get()
    return render_to_response('accounts/people_feeds.html', {'current_user':request.user, 'url_number':url_number, 'student':student, 'STATIC_URL':STATIC_URL}, context_instance=RequestContext(request))

@login_required(login_url='/')
def visit_people_profile(request, url_number):
    student = Student.objects(url_number=url_number).get()
    return render_to_response('accounts/people_profile.html', {'current_user':request.user, 'url_number':url_number, 'student':student, 'STATIC_URL':STATIC_URL}, context_instance=RequestContext(request))

@login_required(login_url='/')
def visit_people_corporation(request, url_number):
    student = Student.objects(url_number=url_number).get()
    return render_to_response('accounts/people_corporation.html', {'current_user':request.user, 'url_number':url_number, 'student':student, 'STATIC_URL':STATIC_URL}, context_instance=RequestContext(request))

@login_required(login_url='/')
def visit_people_group(request, url_number):
    student = Student.objects(url_number=url_number).get()
    return render_to_response('accounts/people_group.html', {'current_user':request.user, 'url_number':url_number, 'student':student, 'STATIC_URL':STATIC_URL}, context_instance=RequestContext(request))

@login_required(login_url='/')
def redirect_to_feeds(request, url_number):
    return HttpResponseRedirect('/people/' + str(url_number) + '/feeds/')



@login_required(login_url='/')
def add_watch_student(request, url_number):
    current_user = request.user
    student = Student.objects(url_number=url_number).get()
    if S_S_Card.objects(user=current_user):
        sc = S_S_Card.objects(user=current_user).get()
    else:
        sc = S_S_Card(user=current_user)
    
    if sc.add_watched_students(student):
        
        return HttpResponse('success')
    else:
        
        return HttpResponse('fail')

@login_required(login_url='/')
def cancle_watch_student(request, url_number):
    current_user = request.user
    student = Student.objects(url_number=url_number).get()
    if S_S_Card.objects(user=current_user):
        sc = S_S_Card.objects(user=current_user).get()
    else:
        sc = S_S_Card(user=current_user)
    
    if sc.cancle_watched_students(student):
        
        return HttpResponse('success')
    else:
        
        return HttpResponse('fail')



