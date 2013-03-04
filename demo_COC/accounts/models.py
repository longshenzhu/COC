# -*- coding: UTF-8 -*-
from mongoengine.django.auth import User
from mongoengine import Document, fields, CASCADE, EmbeddedDocument, PULL
from mongoengine import signals
# Create your models here.


class Public_Profile(EmbeddedDocument):
    realname = fields.StringField()
    face = fields.StringField()
    gender = fields.StringField(max_length=2)
    school = fields.StringField()
    birthday = fields.DateTimeField()

class Private_Profile(EmbeddedDocument):
    phone_number = fields.StringField()
    major = fields.StringField()
    MBTI = fields.StringField()

class Feed(EmbeddedDocument):
    content = fields.StringField()
    creat_time = fields.DateTimeField()

    



class Student(User):
    url_number = fields.IntField()
    public_profile = fields.EmbeddedDocumentField(Public_Profile)
    private_profile = fields.EmbeddedDocumentField(Private_Profile)
    feeds = fields.ListField(fields.EmbeddedDocumentField(Feed))
    
        
    
    def get_sscard(self):
        return S_S_Card.objects(user=self)
    
    def get_sgcard(self):
        return S_G_Card.objects(user=self, is_active=True)
    
    def get_admin_group(self):
        return S_G_Card.objects(user=self, is_active=True,is_admin=True)
    
    def get_in_group(self):
        return S_G_Card.objects(user=self, is_active=True,is_admin=False)
    
    def get_sccard(self):
        return S_C_Card.objects(user=self,is_active=True)
    
    def get_event_list(self):#
        return Event.objects(user=self).get().event
    
    def grouptopics_creat(self):#我创建的话题
        from forum.models import Topic
        return Topic.objects(creator__in=S_G_Card.objects(user=self))
    
    def grouptopics(self):#我关注的小组的话题
        from forum.models import Topic
        return Topic.objects(creator__in=S_G_Card.objects(group__in=self.get_sgcard().scalar('group')))
        
    def grouptopics_reply(self):#我回复的话题
        from forum.models import Post
        return Post.objects(author=self).distinct('topic')
    
    
from corporation.models import Corporation
from group.models import Group   

class S_S_Card(Document):
    user = fields.ReferenceField(Student)
    watched_students = fields.ListField(fields.ReferenceField(Student, reverse_delete_rule=PULL))
    
    def add_watched_students(self, student):  # 添加关注的人
        return self.update(push__watched_students=student)
    
    def cancle_watched_students(self, student):  # 取消关注的人
        return self.update(pull__watched_students=student)
    
    def is_watched_student(self, student):  # 是不是你关注的人
        if student in self.watched_students:
            return True
        else:
            return False
    

class S_C_Card(Document):
    user = fields.ReferenceField(Student)
    department = fields.StringField()#部门
    corporation = fields.ReferenceField(Corporation, reverse_delete_rule=CASCADE)
    creat_time = fields.DateTimeField()#入社时间
    is_active = fields.BooleanField()
    is_admin = fields.BooleanField()#是否是社团管理员
    

class Event(Document):
    user = fields.ReferenceField(Student)
    event = fields.ListField(fields.GenericReferenceField())
    
    @classmethod
    def event_post_save(cls, sender, document, **kwargs):
        Event.objects(user__in=S_S_Card.objects(watched_students__all=[document.user]).scalar('user')).update(push__event=document)
    
class S_G_Card(Document):
    user = fields.ReferenceField(Student)
    group = fields.ReferenceField(Group, reverse_delete_rule=CASCADE)
    creat_time = fields.DateTimeField()
    is_active = fields.BooleanField()#保证退出小组之后话题还在
    is_admin = fields.BooleanField()#是否是小组管理员
    
    def description(self):
        return self.user.public_profile.realname + "加入了" + self.group.name

signals.post_save.connect(Event.event_post_save, sender=S_G_Card)
    

        
