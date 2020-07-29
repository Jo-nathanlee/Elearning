from django.contrib import admin
from .models import Group,GroupPost,GroupComment

# Register your models here.
class GroupAdmin(admin.ModelAdmin):
    list_display = ['get_members','teacher','project','id']

class GroupPostAdmin(admin.ModelAdmin):
    list_display = ['group','title','content']

class GroupCommentAdmin(admin.ModelAdmin):
    list_display = ['post','content']

admin.site.register(Group,GroupAdmin)
admin.site.register(GroupPost,GroupPostAdmin)
admin.site.register(GroupComment,GroupCommentAdmin)