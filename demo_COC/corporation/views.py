# -*- coding: UTF-8 -*-
import os
import datetime
from PIL import Image
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from demo_COC.settings import STATIC_URL, MEDIA_ROOT, MEDIA_URL
from django.http import HttpResponseRedirect
from django.contrib.auth import *
from forms import CreatCorporationForm,ModifyCorporationForm
from models import Corporation
from reply.models import Reply
from reply.forms import NewReplyForm
from topic.models import Topic
from topic.forms import NewTopicForm
from relations.models import S_C_Card
from django.template import RequestContext
from mongoengine.django.sessions import MongoSession
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def creat_corporation(request):
    if request.method == "POST":
        form = CreatCorporationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            introduction = form.cleaned_data['introduction']
            corporation = Corporation(name=name, introduction=introduction, logo=STATIC_URL + 'img/face.png')
            url_number = len(Corporation.objects) + 1
            corporation.url_number = url_number
            corporation.creat_time = datetime.datetime.now()
            if request.FILES:
                path = 'img/corporation/' + str(url_number)
                if not os.path.exists(MEDIA_ROOT + path):
                    os.makedirs(MEDIA_ROOT + path)
                
                img = Image.open(request.FILES['logo'])
                if img.mode == 'RGB':
                    filename = 'logo.jpg'
                elif img.mode == 'P':
                    filename = 'logo.png'
                filepath = '%s/%s' % (path, filename)
                # 获得图像的宽度和高度
                width, height = img.size
                # 计算宽高
                ratio = 1.0 * height / width
                # 计算新的高度
                new_height = int(260 * ratio)
                new_size = (260, new_height)
                # 缩放图像
                out = img.resize(new_size, Image.ANTIALIAS)
                out.save(MEDIA_ROOT + filepath)
                corporation.logo = MEDIA_URL + filepath
                
            corporation.save()
            sccard = S_C_Card(user=request.user, corporation=corporation, is_active=True, is_admin=True,creat_time=datetime.datetime.now())
            sccard.save()
            return HttpResponseRedirect('/corporation/' + str(url_number) + '/')
        
    else:
        form = CreatCorporationForm()
        return render_to_response('corporation/creat_corporation.html', {'form':form, 'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))
                
                 
def corporation(request, gurl_number):
    corporation = Corporation.objects(url_number=gurl_number).get()
    if request.method == "POST":
        form = NewTopicForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            topic = Topic(title=title)
            turl_number = len(Topic.objects) + 1
            topic.url_number = turl_number
            topic.content = content
            topic.creat_time = datetime.datetime.now()
            topic.is_active = True
            topic.is_locked = False
            topic.is_top = False
            topic.clicks = 0
            topic.update_time = datetime.datetime.now()
            topic.update_author = request.user
            sccard = S_C_Card.objects(user=request.user, corporation=corporation).get()
            topic.creator = sccard
            topic.save()
            return HttpResponseRedirect('/corporation/' + str(gurl_number) + '/topic/' + str(turl_number) + '/')
            
            
    else:
        form = NewTopicForm()
        return render_to_response('corporation/corporation.html', {'form':form, 'corporation':corporation, 'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))
        
    
def entercorporation(request, url_number):
    corporation = Corporation.objects(url_number=url_number).get()
    corporation.entercorporation(request.user)
    return HttpResponse('success')
    
def quitcorporation(request, url_number):
    corporation = Corporation.objects(url_number=url_number).get()
    corporation.quitcorporation(request.user)
    return HttpResponse('success')
    
    
def showtopic(request, gurl_number, turl_number):
    corporation = Corporation.objects(url_number=gurl_number).get()
    topic = Topic.objects(url_number=turl_number).get()
    topic.clicks += 1
    topic.save()
    if request.method == 'POST':
        form = NewReplyForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            reply = Reply(content=content)
            sccard = S_C_Card.objects(user=request.user, corporation=corporation).get()
            reply.creator = sccard
            reply.creat_time = datetime.datetime.now()
            reply.target = topic
            reply.is_active = True
            reply.save()
            topic.update_author = request.user
            topic.update_time = datetime.datetime.now()
            topic.save()
            return HttpResponseRedirect('/corporation/' + str(gurl_number) + '/topic/' + str(turl_number) + '/')
        
    else:
        form = NewReplyForm()
        return render_to_response('corporation/corporation_topic.html', {'corporation':corporation, 'current_user':request.user, 'form':form, 'topic':topic, 'STATIC_URL':STATIC_URL}, context_instance=RequestContext(request))

    
def my_corporations_creat(request):
    return render_to_response('corporation/my_corporations_creat.html', {'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))

def my_corporations_news(request):
    return render_to_response('corporation/my_corporations_news.html', {'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))

def my_corporations_reply(request):
    return render_to_response('corporation/my_corporations_reply.html', {'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))
  
def ask_for_admin(request,url_number):
    corporation = Corporation.objects(url_number=url_number).get()
    corporation.ask_for_admin(request.user)
    return HttpResponse('success')
                
                
def corporation_manage_edit(request,url_number):
    corporation = Corporation.objects(url_number=url_number).get()
    if request.method == "POST":
        form = ModifyCorporationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            introduction = form.cleaned_data['introduction']
            corporation.update(set__name=name, set__introduction=introduction)
            if request.FILES:
                path = 'img/corporation/' + str(url_number)
                if not os.path.exists(MEDIA_ROOT + path):
                    os.makedirs(MEDIA_ROOT + path)
                
                img = Image.open(request.FILES['logo'])
                if img.mode == 'RGB':
                    filename = 'logo.jpg'
                elif img.mode == 'P':
                    filename = 'logo.png'
                filepath = '%s/%s' % (path, filename)
                # 获得图像的宽度和高度
                width, height = img.size
                # 计算宽高
                ratio = 1.0 * height / width
                # 计算新的高度
                new_height = int(260 * ratio)
                new_size = (260, new_height)
                # 缩放图像
                out = img.resize(new_size, Image.ANTIALIAS)
                out.save(MEDIA_ROOT + filepath)
                corporation.logo = MEDIA_URL + filepath
                
            corporation.save()
            return HttpResponseRedirect('/corporation/' + str(url_number) + '/')
    else:
        form = ModifyCorporationForm()
        return render_to_response('corporation/corporation_manage_edit.html', {'corporation':corporation, 'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))
  
def corporation_manage_members(request,url_number):
    corporation = Corporation.objects(url_number=url_number).get()
    return render_to_response('corporation/corporation_manage_members.html', {'corporation':corporation, 'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))
  
def corporation_manage_advance(request,url_number):
    corporation = Corporation.objects(url_number=url_number).get()
    return render_to_response('corporation/corporation_manage_advance.html', {'corporation':corporation, 'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))
  
  
def demote(request,corporation_url_number,user_url_number):
    corporation = Corporation.objects(url_number=corporation_url_number).get()
    corporation.demote(user_url_number)
    return HttpResponse('success')
    
    
def promote(request,corporation_url_number,user_url_number):
    corporation = Corporation.objects(url_number=corporation_url_number).get()
    corporation.promote(user_url_number)
    return HttpResponse('success')
    
def kick_out(request,corporation_url_number,user_url_number):
    corporation = Corporation.objects(url_number=corporation_url_number).get()
    corporation.kick_out(user_url_number)
    return HttpResponse('success')
    
    
    
