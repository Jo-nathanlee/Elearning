from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE
    )
    course_pic = models.TextField(null=True,blank=True,default='https://miro.medium.com/max/3336/1*YMFKP8e6kR9cbM3IKXBtLw.png')
    course_introduction = models.TextField(default='')
    teacher = models.ForeignKey(
        'account.User',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    credits = models.IntegerField(default=0)

    def __str__(self):
        return self.course_name

class Lesson(models.Model):
    lesson_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE
    )
    lesson_content =  models.TextField(default='')
    lesson_name = models.CharField(max_length=255)
    lesson_video = models.TextField(default='')
    homework_title = models.CharField(max_length=255,null=True,blank=True)
    homework_description = models.TextField(default='',null=True,blank=True)
    homework_attachment = models.FileField(null=True,blank=True)
    if_compiler = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    lesson = models.ForeignKey(
        'Lesson',
        on_delete=models.SET
    )
    question_id = models.AutoField(primary_key=True)
    question_content = models.TextField(default='')
    questioner = models.ForeignKey(
        'account.User',
        related_name='questioner',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True)
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE
    )
    answer_content = models.TextField(default='')
    answerer = models.ForeignKey(
        'account.User',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

class UserCourse(models.Model):
    user = models.ForeignKey(
        'account.User',
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

class Homework(models.Model):
    lesson_id = models.ForeignKey(
        'Lesson',
        on_delete=models.SET
    )
    student = models.ForeignKey(
        'account.User',
        on_delete=models.CASCADE
    )
    homework = models.FileField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)







    
    
   

