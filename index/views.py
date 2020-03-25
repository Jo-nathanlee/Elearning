from django.shortcuts import render
from account.models import User
from course.models import Course,UserCourse

# Create your views here.
def index(request):
    all_course = Course.objects.all().order_by('-created_at')
    return render(request, 'index.html',locals())

def teacher(request):
    teacher = User.objects.get(email=request.user.email)
    mycourse = Course.objects.filter(teacher=teacher).order_by('-created_at')
    sort = 'newest'

    teacher_course_count = Course.objects.filter(teacher=teacher).count()
    teacher_student_count = UserCourse.objects.filter(course__teacher=teacher).count()

    

    try:
        sort = request.GET.get('sort', 'newest')
        if sort == 'newest':
            mycourse = Course.objects.filter(teacher=teacher).order_by('-created_at')
        else:
            mycourse = Course.objects.filter(teacher=teacher).order_by('created_at') 
    except Exception as e:
        mycourse = Course.objects.filter(teacher=teacher).order_by('-created_at')

    return render(request,'teacher_index.html',locals())

