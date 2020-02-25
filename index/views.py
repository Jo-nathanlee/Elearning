from django.shortcuts import render
from account.models import User
from course.models import Course

# Create your views here.
def index(request):
    return render(request, 'index.html')

def teacher(request):
    teacher = User.objects.get(email=request.user.email)
    mycourse = Course.objects.filter(teacher=teacher).order_by('-created_at')
    sort = 'newest'

    

    try:
        sort = request.GET.get('sort', 'newest')
        if sort == 'newest':
            mycourse = Course.objects.filter(teacher=teacher).order_by('-created_at')
        else:
            mycourse = Course.objects.filter(teacher=teacher).order_by('created_at') 
    except Exception as e:
        mycourse = Course.objects.filter(teacher=teacher).order_by('-created_at')

    return render(request,'teacher_index.html',locals())

