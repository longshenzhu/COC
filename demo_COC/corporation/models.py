# -*- coding: UTF-8 -*-
from mongoengine import Document, fields, PULL
from accounts.models import Student


# Create your models here.


class Corporation(Document):
    url_number = fields.IntField()
    name = fields.StringField(required=True, verbose_name=u'社团名称')
    logo = fields.StringField()  # logo路径
    birthyear = fields.IntField()  # 创建年份
    departments = fields.ListField(fields.StringField())
    introduction = fields.StringField(required=True, verbose_name=u'社团简介')
    tags = fields.ListField(fields.StringField())  # 社团标签
    school = fields.StringField()
    who_watches = fields.ListField(fields.ReferenceField(Student, reverse_delete_rule=PULL))
    
    def get_member_list(self):#得到社团普通成员列表
        from accounts.models import S_C_Card
        return S_C_Card.objects(corporation=self, is_active=True,is_admin=False).scalar('user')
        
    def get_admin_list(self):#得到社团管理员列表
        from accounts.models import S_C_Card
        return S_C_Card.objects(corporation=self, is_active=True,is_admin=True).scalar('user')
    
    def get_user_list(self):  # 得到社团所有成员列表
        from accounts.models import S_C_Card
        return S_C_Card.objects(corporation=self, is_active=True).scalar('user')
        
    def get_topic_list(self):  # 得到论坛主题列表
        from accounts.models import S_C_Card
        creator = S_C_Card.objects(corporation=self).all()
        from forum.models import Topic
        return Topic.objects(creator__in=creator)
    
    def get_inactive_topic_list(self):#得到删除主题列表
        from accounts.models import S_C_Card
        creator = S_C_Card.objects(corporation=self).all()
        from forum.models import Topic
        return Topic.objects(creator__in=creator,is_active=False)
    
    def get_activity_list(self):  # 得到活动列表
        from activity.models import Activity
        return Activity.objects(sponsor=self).all()
        
    
    
    
    
