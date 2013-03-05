# -*- coding: UTF-8 -*-
from mongoengine import Document, fields, PULL
from corporation.models import Corporation
from accounts.models import Student
from mongoengine import signals
import datetime
# Create your models here.



class Activity(Document):
    name = fields.StringField(required=True, verbose_name=u'活动名称')
    poster = fields.ImageField()  # 活动海报
    file = fields.FileField()  # 活动文件，供上传下载
    
    detail = fields.StringField(required=True, verbose_name=u'活动详情')
    sponsor = fields.ReferenceField(Corporation, required=True)  # 发起人
    
    
    who_likes = fields.ListField(fields.ReferenceField(Student, reverse_delete_rule=PULL))  # 喜欢活动的人
    who_entered = fields.ListField(fields.ReferenceField(Student, reverse_delete_rule=PULL))  # 参加这个活动的人
    total_students = fields.IntField()  # 参加活动总人
    clicks = fields.IntField()  # 点击数
    
    def liked_activity(self, student):  # 喜欢活动
        return self.update(push__liked_activity=student)

    
    
    
    
class Date(Document):
    start_time = fields.DateTimeField()
    finish_time = fields.DateTimeField()
    place = fields.StringField(required=True, verbose_name=u'活动地点')
    max_student = fields.IntField(required=True)  # 人数上限
    
    who_entered = fields.ListField(fields.ReferenceField(Student, reverse_delete_rule=PULL))  # 此时间段参加的人
    students_number = fields.IntField()  # 此时间段参加人数
    
    activity = fields.ReferenceField(Activity)  # 活动
    
    def enter(self, activity, student):  # 参加活动
        activity.update(push__who_entered=student)
        activity.update(inc__total_students=1)
        self.update(inc__students_number=1)
        return self.update(push__who_entered=activity)
    
    def is_finished(self):  # 判断是否已经结束
        if self.finish_time < datetime.datetime.now():
            return True
        else:
            return False
        
    def start_count_down(self):  # 开始倒计时
        return self.start_time - datetime.datetime.now()
        
        
    
