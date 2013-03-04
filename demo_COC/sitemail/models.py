from accounts.models import Student
from mongoengine import Document, fields, CASCADE
# Create your models here.
class Sitemail(Document):
    title = fields.StringField()
    content = fields.StringField()
    creat_time = fields.DateTimeField()
    reciver = fields.ReferenceField(Student, reverse_delete_rule=CASCADE)
