from accounts.models import Student
from mongoengine import Document, fields, CASCADE
# Create your models here.
class Sitemail(Document):
    title = fields.StringField()
    content = fields.StringField()
    creat_time = fields.DateTimeField()
    author = fields.ReferenceField(Student, reverse_delete_rule=CASCADE)
    reciver = fields.ListField(fields.ReferenceField(Student, reverse_delete_rule=CASCADE))
