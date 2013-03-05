# -*- coding: UTF-8 -*-   
from accounts.models import Student, S_G_Card
from mongoengine import Document, fields, DO_NOTHING, CASCADE
# Create your models here.

class Topic(Document):
    title = fields.StringField(verbose_name=u'标题')
    content = fields.StringField(verbose_name=u'内容')
    url_number = fields.IntField()
    creator = fields.GenericReferenceField()  # 发布人S_G_Card, reverse_delete_rule=DO_NOTHING
    creat_time = fields.DateTimeField()  # 发布时间
    
    update_time = fields.DateTimeField()  # 更新时间
    update_author = fields.ReferenceField(Student, reverse_delete_rule=DO_NOTHING)  #最后回复作者
    
    clicks = fields.IntField()  #浏览数
    
    is_active = fields.BooleanField(verbose_name=u'可见')
    is_locked = fields.BooleanField(verbose_name=u'锁帖')
    is_top = fields.BooleanField(verbose_name=u'置顶')
    
    def get_post_list(self):
        return Post.objects(topic=self).all()
    
    def replys(self):
        return Post.objects(topic=self).count()
    
    def top(self):#置顶
        self.is_top = True
        
    def untop(self):
        self.is_top = False
        
    def lock(self):#禁止回复
        self.is_locked = True
        
    def unlock(self):
        self.is_locked = False
        
    def inactive(self):#设为不可见
        self.is_active = False

    def active(self):#设为可见
        self.is_active = True

class Post(Document):
    content = fields.StringField(verbose_name=u'内容')
    author = fields.ReferenceField(Student, reverse_delete_rule=DO_NOTHING)  #作者
    creat_time = fields.DateTimeField()  # 发布时间
    floor = fields.IntField()  # 楼层
    is_active = fields.BooleanField(verbose_name=u'可见')
    topic = fields.ReferenceField(Topic, reverse_delete_rule=CASCADE)
    
    def inactive(self):#设为不可见
        self.is_active = False
        
    def active(self):#设为可见
        self.is_active = True
    

