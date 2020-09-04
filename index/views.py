from django.shortcuts import render
from account.models import User
from course.models import Course,UserCourse,Category,Review
from django.db.models import Avg

# Get programming language categories
def get_language():
    model_category = Category.objects.all()
    return model_category

def index(request):
    all_course = Course.objects.all().order_by('-created_at')
    category = get_language()
    return render(request, 'index.html',locals())

def teacher(request):
    category = get_language()
    teacher = User.objects.get(email=request.user.email)
    mycourse = Course.objects.filter(teacher=teacher).order_by('-created_at')
    sort = 'newest'

    teacher_course_count = Course.objects.filter(teacher=teacher).count()
    teacher_student_count = UserCourse.objects.filter(course__teacher=teacher).count()
    teacher_rating = Review.objects.filter(course__teacher=teacher).aggregate(Avg('rating'))
    if teacher_rating['rating__avg'] != None or teacher_rating != 'None':
        teacher_rating = format(teacher_rating['rating__avg'], '.1f')
    else:
        teacher_rating = ''
    

    try:
        sort = request.GET.get('sort', 'newest')
        if sort == 'newest':
            mycourse = Course.objects.filter(teacher=teacher).order_by('-created_at')
        else:
            mycourse = Course.objects.filter(teacher=teacher).order_by('created_at') 
    except Exception as e:
        mycourse = Course.objects.filter(teacher=teacher).order_by('-created_at')

    return render(request,'teacher_index.html',locals())

