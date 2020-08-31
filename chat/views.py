# chat/views.py
from django.shortcuts import render,redirect,HttpResponse
from django.utils.safestring import mark_safe
import json
from .models import Message
from account.models import User
from group.models import Group
from django.contrib.auth import authenticate
from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden



def room(request, group_id):
    group = Group.objects.get(id=group_id)
    user = User.objects.get(email=request.user.email)
    group_num = group.group_num
    
    if request.user in group.member.all() or request.user == group.teacher:
        chat_messages = Message.objects.filter(group=group_id).order_by("timestamp")
        return render(request, 'chat/room.html', {
            'chat_messages': chat_messages,
            'group_id': group_id
        })
    else:   
        return HttpResponseForbidden("403 Forbidden , 您沒有權限訪問！")

