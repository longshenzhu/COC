'''
Created on 2013-1-29

@author: lcy
'''
from django.conf.urls import url, patterns
urlpatterns = patterns('corporation.views',
    url(r'^my_corporations_news/$','my_corporations_news'),
    url(r'^my_corporations_reply/$','my_corporations_reply'),
    url(r'^my_corporations_creat/$','my_corporations_creat'),
    url(r'^creat_corporation/$', 'creat_corporation'),
    url(r'^(\d+)/$', 'corporation'),
    url(r'^(\d+)/enter/$', 'entercorporation'),
    url(r'^(\d+)/quit/$', 'quitcorporation'),
    url(r'^(\d+)/topic/(\d+)/$', 'showtopic'),
    url(r'^(\d+)/ask/$','ask_for_admin'),
    url(r'^(\d+)/manage_edit/$','corporation_manage_edit'),
    url(r'^(\d+)/manage_members/$','corporation_manage_members'),
    url(r'^(\d+)/manage_advance/$','corporation_manage_advance'),
    url(r'^(?P<corporation_url_number>\d+)/promote/(?P<user_url_number>\d+)/$','promote'),
    url(r'^(?P<corporation_url_number>\d+)/demote/(?P<user_url_number>\d+)/$','demote'),
    url(r'^(?P<corporation_url_number>\d+)/kick_out/(?P<user_url_number>\d+)/$','kick_out'),
)