from django.contrib import admin
from .models import Category,Course,Lesson,Question,Answer,UserCourse,Homework,Note,Review
# Register your models here.

class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_id','course_name','category','course_pic','course_introduction','teacher','created_at']

class LessonAdmin(admin.ModelAdmin):
    list_display = ['lesson_id','course','lesson_content','lesson_name','lesson_video','homework_title','homework_description','homework_attachment','if_compiler','created_at']

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_id','lesson','question_content','questioner','created_at']

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['answer_id','question','answer_content','answerer','created_at']

class UserCourseAdmin(admin.ModelAdmin):
    list_display = ['user','course']

class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['lesson','student','homework','created_at']

class NoteAdmin(admin.ModelAdmin):
    list_display = ['lesson','student','note','created_at']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['course','reviewer','review','rating','created_at']

admin.site.register(Category)
admin.site.register(Course,CourseAdmin)
admin.site.register(Lesson,LessonAdmin)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer,AnswerAdmin)
admin.site.register(UserCourse,UserCourseAdmin)
admin.site.register(Homework,HomeworkAdmin)
admin.site.register(Note,NoteAdmin)
admin.site.register(Review,ReviewAdmin)