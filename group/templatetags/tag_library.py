from django import template
from django.utils.safestring import mark_safe
from course.models import Category,Course,UserCourse,Review
from account.models import User

register = template.Library()

@register.inclusion_tag("teacher.html")
def teacher(email):
    teacher = User.objects.get(email=email)
    teacher_course_count = Course.objects.filter(teacher=teacher).count()
    teacher_student_count = UserCourse.objects.filter(course__teacher=teacher).count()
    teacher_rating = Review.objects.filter(course__teacher=teacher).aggregate(Avg('rating'))
    teacher_rating = teacher_rating['rating__avg']
    return {'teacher': teacher,'teacher_course_count': teacher_course_count,'teacher_student_count': teacher_student_count,'teacher_rating': teacher_rating }