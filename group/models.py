from django.db import models

# Create your models here.
class Group(models.Model):
    member = models.ManyToManyField('account.User')
    teacher = models.ForeignKey(
        'account.User',
        on_delete=models.CASCADE,related_name='group_teacher'
    )
    project = models.FileField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Group '+self.course_name

class GroupPost(models.Model):
    group = models.ForeignKey(
        'Group',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255,default='')
    content = models.TextField(default='')
    
class GroupComment(models.Model):
    post = models.ForeignKey(
        'GroupPost',
        on_delete=models.CASCADE
    )
    content = models.TextField(default='')