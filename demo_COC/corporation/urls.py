'''
Created on 2013-1-29

@author: lcy
'''
from django.conf.urls import url, patterns
urlpatterns = patterns('corporation.views',
    url(r'^$', 'index'),
    url(r'^logout/$', 'userlogout'),
    url(r'^accounts/',),
    url(r'^people/(\d+)/',),
    url(r'^people/(\d+)/profile/'),
    url(r'^people/(\d+)/corporation/'),
    url(r'^people/(\d+)/group/'),
)
