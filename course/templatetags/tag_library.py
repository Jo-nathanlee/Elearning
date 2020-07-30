from django import template
from django.utils.safestring import mark_safe
from course.models import Category,Course,UserCourse,Review
from account.models import User

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
def teacher():
    teacher = User.objects.get(email=request.user.email)
    teacher_course_count = Course.objects.filter(teacher=teacher).count()
    teacher_student_count = UserCourse.objects.filter(course__teacher=teacher).count()
    teacher_rating = Review.objects.filter(course__teacher=teacher).aggregate(Avg('rating'))
    teacher_rating = teacher_rating['rating__avg']
    return {'teacher': teacher,'teacher_course_count': teacher_course_count,'teacher_student_count': teacher_student_count,'teacher_rating': teacher_rating }