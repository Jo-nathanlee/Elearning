from django import template
from django.utils.safestring import mark_safe
from course.models import Category,Course,UserCourse,Review
from account.models import User
from group.models import Group
from django.db.models import Avg
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect


register = template.Library()

@register.filter
def get_filename(value):
    return str(value).replace("files/","")
@register.filter
def to_int(value):
    return int(value)
@register.filter
def to_str(value):
    return str(value)
@register.filter
def youtube_url(value):
    if value != '':
        return 'https://www.youtube.com/watch?v='+value
    return value
@register.inclusion_tag("all_categories.html")
def get_categories():
    return {'categories': Category.objects.all() }
@register.inclusion_tag("teacher.html")
def teacher(email):
    teacher = User.objects.get(email=email)
    teacher_course_count = Course.objects.filter(teacher=teacher).count()
    if int(teacher_course_count) > 1:
        text_course = str(teacher_course_count)+' Courses'
    else:
        text_course = str(teacher_course_count)+' Course'

    teacher_student_count = UserCourse.objects.filter(course__teacher=teacher).count()
    if int(teacher_student_count) > 1:
        text_student = str(teacher_student_count)+' Students'
    else:
        text_student = str(teacher_student_count)+' Student'

    teacher_rating = Review.objects.filter(course__teacher=teacher).aggregate(Avg('rating'))
    teacher_rating = teacher_rating['rating__avg']
    return {'teacher': teacher,'text_course': text_course,'text_student': text_student,'teacher_rating': teacher_rating }


@register.simple_tag(takes_context=True)
def has_group(context):
    try:
        request = context['request']
        group_id = None
        groups = Group.objects.all()
        for group in groups:
            if request.user in group.member.all():
                my_group = Group.objects.filter(member=request.user).first()
                group_id = my_group.id

        return group_id
    except:
        return None

@register.simple_tag(takes_context=True)
def if_teacher(context):
    try:
        request = context['request']
        if_teacher = Course.objects.filter(teacher=request.user).count()
        if if_teacher>0:
            return True
        else:
            return False
    except:
        return None


