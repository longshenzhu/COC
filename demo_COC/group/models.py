# -*- coding: UTF-8 -*-
from mongoengine import Document, fields
import datetime
# Create your models here.
class Group(Document):
    url_number = fields.IntField()
    name = fields.StringField(required=True, verbose_name=u'小组名称')
    logo = fields.StringField()  # logo路径
    birthday = fields.DateTimeField()  # 创建日期
    introduction = fields.StringField(required=True, verbose_name=u'小组介绍')
    # tags = fields.ListField(fields.StringField())#小组标签
    # school = fields.StringField()
    grouptype = fields.StringField()  # 小组类型，是否为私密小组
    
    def get_topic_list(self):
        from accounts.models import S_G_Card
        creator = S_G_Card.objects(group=self).all()
        from forum.models import Topic
        return Topic.objects(creator__in=creator,is_active=True)
    
    def get_inactive_topic_list(self):
        from accounts.models import S_G_Card
        creator = S_G_Card.objects(group=self).all()
        from forum.models import Topic
        return Topic.objects(creator__in=creator,is_active=False)
    
    def get_member_list(self):
        from accounts.models import S_G_Card
        return S_G_Card.objects(group=self, is_active=True,is_admin=False).scalar('user')
        
    def get_admin_list(self):
        from accounts.models import S_G_Card
        return S_G_Card.objects(group=self, is_active=True,is_admin=True).scalar('user')
    
    def get_user_list(self):
        from accounts.models import S_G_Card
        return S_G_Card.objects(group=self, is_active=True).scalar('user')
        
    def demote(self,user_url_number):
        from accounts.models import Student
        from accounts.models import S_G_Card
        user = Student.objects(url_number=user_url_number).get()
        S_G_Card.objects(group=self,user=user).update(set__is_admin=False)
    
    
    def promote(self,user_url_number):
        from accounts.models import Student
        from accounts.models import S_G_Card
        user = Student.objects(url_number=user_url_number).get()
        S_G_Card.objects(group=self,user=user).update(set__is_admin=True)
        
    def kick_out(self,user_url_number):
        from accounts.models import Student
        from accounts.models import S_G_Card
        user = Student.objects(url_number=user_url_number).get()
        S_G_Card.objects(group=self,user=user).update(set__is_active=False)
        
    def ask_for_admin(self,user):
        from accounts.models import S_G_Card
        if not S_G_Card.objects(group=self, is_active=True,is_admin=True).scalar('user'):
            S_G_Card.objects(user=user, group=self, is_active=True).update(set__is_admin=True)
            
    
    def entergroup(self, user):
        from accounts.models import S_G_Card
        if S_G_Card.objects(group=self, is_active=True,is_admin=False).scalar('user') or S_G_Card.objects(group=self, is_active=True,is_admin=True).scalar('user'):
            if S_G_Card.objects(user=user, group=self):
                S_G_Card.objects(user=user, group=self).update(set__is_active=True, set__is_admin=False, set__creat_time=datetime.datetime.now())
            else:
                S_G_Card(user=user, group=self, is_active=True, is_admin=False,creat_time=datetime.datetime.now()).save()
        else:
            if S_G_Card.objects(user=user, group=self):
                S_G_Card.objects(user=user, group=self).update(set__is_active=True, set__is_admin=True,set__creat_time=datetime.datetime.now())
            else:
                S_G_Card(user=user, group=self, is_active=True,is_admin=True, creat_time=datetime.datetime.now()).save()
        
        
    def quitgroup(self, user):
        from accounts.models import S_G_Card
        S_G_Card.objects(user=user, group=self, is_active=True).update(set__is_active=False)
        
