from django.shortcuts import render,redirect,HttpResponse
from django.http import FileResponse,JsonResponse
from account import models, forms
from course.models import Homework
from django.contrib.auth import authenticate
from django.contrib import auth,messages
from pprint import pprint
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
import json
import base64
from django.core.files.base import ContentFile
import os
from django.conf import settings


# Create your views here.
# 個人資料
def account(request):
    if request.method == "POST":
        try:
            email= request.user.email
            name = request.POST['name']
            birthday = request.POST['birthday']
            sex = request.POST['sex']
            language_learnt = request.POST['language_learnt']
            self_introduction = request.POST['self_introduction']

            data = {
                'name':name,
                'birthday':birthday,
                'sex':sex,
                'language_learnt':language_learnt,
                'self_introduction':self_introduction
            }
            model_user = models.User.objects.get(email=email)
            model_user.__dict__.update(**data)
            model_user.save()
        except Exception as e:
            pass



    tab = "index"
    User = models.User.objects.get(email= request.user.email)
    return render(request, 'account.html', locals())
#修改照片&顯示作業
def account_tab(request,tab):
    tab = tab
    email= request.user.email
    user = models.User.objects.get(email=email)  
    if tab == "pic":
        if request.method == "POST":
            try:
                # pic = request.POST['picture']
                # arr_json = json.loads(pic)
                # json_data = arr_json['data']
                # file_name = arr_json['name']

                # if file_name not in str(user.pic):
                #     data = ContentFile(base64.b64decode(json_data))  
                #     user.pic.save(file_name, data, save=True)
                #user.save()
                pic_url = request.POST['pic_url']
                models.User.objects.filter(email=email).update(pic=pic_url)
                data = {}
                return JsonResponse(data,safe=False)
                messages.add_message(request, messages.INFO, '更新成功！')
                
            except Exception as e:
                messages.add_message(request, messages.ERROR, '更新失敗！')
                pass
            
            

    if tab == "homework":
        homework = Homework.objects.filter(student = request.user)
    return render(request, 'account.html',locals())


def register(request):
    if request.method == "POST":
        accountForm = forms.AccountForm(request.POST)
        if accountForm.is_valid():
            try:
                name = request.POST['name']
                email = request.POST['email']
                password = request.POST['password']
                birthday = request.POST['birthday']
                sex = request.POST['sex']
                language_learnt = request.POST['language_learnt']

                user_email = list(models.User.objects.all().values_list('email'))
                for i in user_email:
                    if email in i:
                        raise forms.ValidationError('帳號已存在，請重新輸入！')
            
                model_user = models.User.objects.create(username=name,name=name,email=email,password=make_password(password),birthday=birthday,sex=sex,language_learnt=language_learnt)
                model_user.save()

                user = auth.authenticate(email=email,password=password)
                if user is not None:
                    auth.login(request,user)
                    messages.add_message(request, messages.INFO, '註冊成功！')
                    return redirect('/index/')
            except Exception as e:
                messages.add_message(request, messages.ERROR, '欄位格式錯誤！')
        else:
            messages.add_message(request, messages.ERROR, '欄位格式錯誤！')
    if request.user.is_authenticated:
        return redirect('/index/',locals())
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(request,user)
            message = '登入成功！'
            return redirect('/index/',locals())
        else:
            messages.add_message(request, messages.ERROR, '帳號密碼錯誤，請重新登入！')

    if request.user.is_authenticated:
        return redirect('/index/',locals())
    return render(request,"login.html",locals())

def logout(request):
	auth.logout(request)
	return redirect('/user/login/')	

def download(request,id):
    homework = Homework.objects.get(id=id)
    filename = str(homework.homework).replace("files/","")
    filename = filename.encode('utf-8').decode('ISO-8859-1')
    
    file=open(os.path.join(settings.MEDIA_ROOT, str(homework.homework)),'rb')
    response =FileResponse(file)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="'+filename+'"'
    return response

