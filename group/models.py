from django.db import models
from datetime import datetime    
# Create your models here.
class Group(models.Model):
    member = models.ManyToManyField('account.User')
    teacher = models.ForeignKey(
        'account.User',
        on_delete=models.CASCADE,related_name='group_teacher'
    )
    course = models.ForeignKey(
        'course.Course',
        on_delete=models.CASCADE,null=True
    )
    group_num = models.IntegerField(null=True)
    project = models.FileField(null=True,blank=True)
    project_url = models.TextField(default='',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Group '+str(self.id)
    
    def get_members(self):
        return "\n".join([member.name for member in self.member.all()])

class GroupPost(models.Model):
    group = models.ForeignKey(
        'Group',
        on_delete=models.CASCADE
    )
    creator =  models.ForeignKey(
        'account.User',
        on_delete=models.CASCADE,
        null=True,
    )
    title = models.CharField(max_length=255,default='')
    content = models.TextField(default='')
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    
class GroupComment(models.Model):
    post = models.ForeignKey(
        'GroupPost',
        on_delete=models.CASCADE
    )
    creator =  models.ForeignKey(
        'account.User',
        on_delete=models.CASCADE,
        null=True,
    )
    content = models.TextField(default='')
    created_at = models.DateTimeField(default=datetime.now, blank=True)
