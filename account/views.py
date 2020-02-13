from django.shortcuts import render,redirect,HttpResponse
from account import models, forms
from django.contrib.auth import authenticate
from django.contrib import auth
from pprint import pprint
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
import json
import base64
from django.core.files.base import ContentFile


# Create your views here.
def account(request):
    if request.method == "POST":
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



    tab = "index"
    User = models.User.objects.get(email= request.user.email)
    return render(request, 'account.html', locals())
def account_tab(request,tab):
    tab = tab
    email= request.user.email
    if request.method == "POST":
        if tab == "pic":
            pic = request.POST['picture']
            arr_json = json.loads(pic)
            json_data = arr_json['data']
            file_name = arr_json['name']
            pic_base64 = "data:"+arr_json['type']+":base64,"+json_data
            imgstr = pic_base64.split(';base64,')


            data = ContentFile(base64.b64decode(json_data))  
            user = models.User.objects.get(email=email)
            user.pic.save(file_name, data, save=True) # image is User's model field
            
            image = models.User.objects.filter(email=email).update(pic=data)
    
    user = models.User.objects.get(email=email)       
    image = user.pic
    return render(request, 'account.html',locals())


def register(request):
    if request.method == "POST":
        accountForm = forms.AccountForm(request.POST)
        if accountForm.is_valid():
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
                message = '註冊成功！'
                return redirect('/index/')
        else:
            message = '欄位格式錯誤！'
            return render(request, 'register.html',locals())
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
            message = '帳號密碼錯誤，請重新登入！'

    if request.user.is_authenticated:
        return redirect('/index/',locals())
    return render(request,"login.html",locals())

def logout(request):
	auth.logout(request)
	return redirect('/user/login/')	

