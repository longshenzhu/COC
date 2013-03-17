from relations.models import S_S_Card
from mongoengine import Document, fields, signals, CASCADE
# Create your models here.
class Sitemail(Document):
    title = fields.StringField()
    content = fields.StringField()
    creat_time = fields.DateTimeField()
    creator = fields.ReferenceField(S_S_Card, reverse_delete_rule=CASCADE)
    is_readed = fields.BooleanField()

from accounts.models import Student
signals.post_save.connect(Student.add_alert_sitemail, sender=Sitemail)