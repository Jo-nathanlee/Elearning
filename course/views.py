from django.shortcuts import render
from . import models
from account.models import User
from group.models import Group
from django.contrib import messages
import json
import math
import base64
from django.core.files.base import ContentFile
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.core import serializers
from django.forms.models import model_to_dict
from django.core.files.base import ContentFile
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
import os
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.db.models import Avg
from distutils.util import strtobool
import botocore
import boto3
import requests
from wsgiref.util import FileWrapper
from django.http import Http404, HttpResponse

# Get programming language categories
def get_language():
    model_category = models.Category.objects.all()
    return model_category

# create a new course
@permission_required('course.can_access', raise_exception = True )
def new_course(request):
    # creating
    if request.method == "POST":
        try:
            course_name = request.POST['course_name']
            category = request.POST['category']
            course_introduction = request.POST['course_introduction']
            pic_url = request.POST['pic_url']

            # picture = request.POST['picture']
            # arr_json = json.loads(picture)
            # json_data = arr_json['data']
            # file_name = arr_json['name']
            # pic_data = ContentFile(base64.b64decode(json_data))  


            #foreign key
            model_category = models.Category.objects.get(category_name=category)  
            teacher = User.objects.get(email=request.user.email) 



            model_course = models.Course.objects.create(
                course_name=course_name,
                category=model_category,
                course_introduction=course_introduction,
                teacher=teacher,
                course_pic=pic_url,
            )
            model_course.save()

            messages.add_message(request, messages.INFO, '新增成功！')
            return HttpResponseRedirect('/course/edit/'+str(model_course.course_id)+'/')
        except Exception as e:
            messages.add_message(request, messages.ERROR, '新增失敗！')

        

    #showing creating page
    category = get_language()
    return render(request, 'new-course.html',locals())

# course index page
def course_index(request):
    # default
    all_course = models.Course.objects.all().order_by('-created_at')
    # search by keyword
    if request.method == 'POST':
        keyword = request.POST['keyword']
        all_course = models.Course.objects.filter(course_name__icontains=keyword).order_by('-created_at')

    

    paginator = Paginator(all_course, 6)
    current_page = int(request.GET.get('page', 1))

    course_count = paginator.count
    page = paginator.num_pages
    
    try:
        if page > 11:
            if current_page_num-5 < 1:
                page_range = range(1, 11)
            elif current_page_num + 5 > paginator.num_pages:
                page_range = range(paginator.num_pages-10, paginator.num_pages + 1)
            else:
                page_range = range(current_page_num-5, current_page_num+6)
        else:
            page_range = paginator.page_range
    except Exception as e:
        page_range = paginator.page_range

    try:
        courses = paginator.page(current_page)
    except EmptyPage as e:
        courses = paginator.page(1)
    except PageNotAnInteger:
        courses = paginator.page(1)

    for c in courses:
        course = models.Course.objects.get(course_id=c.course_id)
        course_rating = models.Review.objects.filter(course=course).aggregate(Avg('rating'))
        if course_rating['rating__avg'] != None:
            rating = int(course_rating['rating__avg'])
            c.rating = range(rating) 
        else:
            c.rating = None


    category = get_language()
    latest_course = models.Course.objects.all().order_by('-created_at')

    return render(request,'courses.html',locals())

# showing my course
def user_course(request):
    all_course = models.UserCourse.objects.filter(user = request.user).order_by('-created_at')
    paginator = Paginator(all_course, 6)
    current_page = int(request.GET.get('page', 1))
    course_count = paginator.count
    page = paginator.num_pages
    
    try:
        if page > 11:
            if current_page_num-5 < 1:
                page_range = range(1, 11)
            elif current_page_num + 5 > paginator.num_pages:
                page_range = range(paginator.num_pages-10, paginator.num_pages + 1)
            else:
                page_range = range(current_page_num-5, current_page_num+6)
        else:
            page_range = paginator.page_range
    except Exception as e:
        page_range = paginator.page_range

    try:
        courses = paginator.page(current_page)
    except EmptyPage as e:
        courses = paginator.page(1)
    except PageNotAnInteger:
        courses = paginator.page(1)

    for c in courses:
        course = models.Course.objects.get(course_id=c.course_id)
        course_rating = models.Review.objects.filter(course=course).aggregate(Avg('rating'))
        if course_rating['rating__avg'] != None:
            rating = int(course_rating['rating__avg'])
            c.rating = range(rating) 
        else:
            c.rating = None


    latest_course = models.Course.objects.all().order_by('-created_at')
    category = get_language()

    return render(request,'user-courses.html',locals())

# click language category in course page
def category(request,category):
    model_category = models.Category.objects.get(category_name = category)
    all_course = models.Course.objects.filter(category=model_category)
    paginator = Paginator(all_course, 6)
    current_page = int(request.GET.get('page', 1))
    course_count = paginator.count
    page = paginator.num_pages

    try:
        if page > 11:
            if current_page_num-5 < 1:
                page_range = range(1, 11)
            elif current_page_num + 5 > paginator.num_pages:
                page_range = range(paginator.num_pages-10, paginator.num_pages + 1)
            else:
                page_range = range(current_page_num-5, current_page_num+6)
        else:
            page_range = paginator.page_range
    except Exception as e:
        page_range = paginator.page_range

    try:
        courses = paginator.page(current_page)
    except EmptyPage as e:
        courses = paginator.page(1)
    except PageNotAnInteger:
        courses = paginator.page(1)

    latest_course = paginator.page(1)
    category = get_language()

    return render(request,'courses.html',locals())

# single course page
def course_page(request,course_id):
    course_id = course_id
    course = models.Course.objects.get(course_id=course_id)
    teacher = User.objects.get(email=course.teacher)
    user = User.objects.get(email=request.user.email)
    user_course = models.UserCourse.objects.filter(course=course,user=user).count()
    is_teacher = True if teacher.email == request.user.email else False
    registered = True if user_course > 0 else False

    teacher_course_count = models.Course.objects.filter(teacher=course.teacher).count()
    teacher_student_count = models.UserCourse.objects.filter(course__teacher=course.teacher).count()
    lesson = models.Lesson.objects.filter(course=course).order_by('created_at')
    user_course = models.UserCourse.objects.filter(course=course)
    category = get_language()

    if_review = models.Review.objects.filter(reviewer=user,course=course).count()
    review = models.Review.objects.filter(course=course)
    teacher_rating = models.Review.objects.filter(course__teacher=course.teacher).aggregate(Avg('rating'))

    if teacher_rating['rating__avg'] == None or teacher_rating == 'None':
        teacher_rating = ''
    else:
        teacher_rating = format(teacher_rating['rating__avg'], '.1f')
    course_rating = models.Review.objects.filter(course=course).aggregate(Avg('rating'))
    if course_rating['rating__avg'] != None :
        rating_range = range(int(course_rating['rating__avg']))


    return render(request,'single-course.html',locals())

# edit course
@permission_required('course.can_access', raise_exception = True )
def course_edit(request,course_id):
    course = models.Course.objects.get(course_id=course_id)
    category = get_language()
    lesson = models.Lesson.objects.filter(course=course).order_by('created_at')

    # updating course
    if request.method == "POST":
        try:
            category_name = request.POST['category']
            model_category = models.Category.objects.get(category_name=category_name)  
            course.course_name = request.POST['course_name']
            course.category = model_category
            course.course_introduction = request.POST['course_introduction']
            course.course_pic = request.POST['pic_url']
            course.save()
            messages.add_message(request, messages.INFO, '編輯成功！')
            return HttpResponseRedirect('/course/edit/'+str(course_id)+'/')
        except Exception as e:
            messages.add_message(request, messages.ERROR, '編輯失敗！')
    # showing edit page
    return render(request,'edit-course.html',locals())

# delete course
@permission_required('course.can_access', raise_exception = True )
def course_delete(request,course_id):
    try:
        course = models.Course.objects.get(course_id=course_id)
        lesson = models.Lesson.objects.filter(course=course)
        lesson.delete()
        course.delete()
        messages.add_message(request, messages.INFO, '刪除成功！')
    except Exception as e:
        messages.add_message(request, messages.ERROR, '刪除失敗！')
    return HttpResponseRedirect('/index/teacher')

# delete lesson
@permission_required('course.can_access', raise_exception = True )
def lesson_delete(request,lesson_id):
    try: 
        lesson = models.Lesson.objects.get(lesson_id=lesson_id)
        course_id = lesson.course.course_id
        lesson.delete()
        messages.add_message(request, messages.INFO, '刪除成功！')
    except Exception as e:
        messages.add_message(request, messages.ERROR, '刪除失敗！')
    return HttpResponseRedirect('/course/edit/'+str(course_id)+'/')

# new lesson
@permission_required('course.can_access', raise_exception = True )
def new_lesson(request,course_id):
    course_id = course_id
    category = get_language()

    # creating lesson
    if request.method == 'POST':
        try:
            lesson_name = request.POST['lesson_name']
            lesson_video = request.POST['lesson_video']
            # 擷取youtube id
            try:
                if 'youtu.be/' in lesson_video:
                    temp = lesson_video.split('be/')
                    url = temp[1]
                else:
                    temp = lesson_video.split('v=')
                    url = temp[1]
                    temp = url.split('&')
                    url = temp[0]
            except Exception as e:
                url = ''
            lesson_content = request.POST['text-editor']
            homework_title = request.POST['homework_title']
            homework_description = request.POST['homework_description']
            if_compiler = request.POST['if_compiler']

            

            course = models.Course.objects.get(course_id = course_id)

            lesson = models.Lesson.objects.create(
                course=course,
                lesson_name=lesson_name,
                lesson_video=url,
                lesson_content=lesson_content,
                homework_title=homework_title,
                homework_description=homework_description,
                if_compiler=eval(if_compiler)
            )
            
            homework_file = request.POST['filepond']
            if homework_file != "":
                arr_json = json.loads(homework_file)
                file_data = arr_json['data']
                file_name = arr_json['name']
                file_data = ContentFile(base64.b64decode(file_data))  
                lesson.homework_attachment.save(file_name, file_data, save=True)

            
            lesson.save()
            messages.add_message(request, messages.INFO, '新增成功！')
            return HttpResponseRedirect('/course/edit/'+str(course_id)+'/')

        except Exception as e:
            messages.add_message(request, messages.ERROR, '新增失敗！')
    # showing creating page
    return render(request,'edit-lesson.html',locals())

# edit lesson
@permission_required('course.can_access', raise_exception = True )
def edit_lesson(request,course_id,lesson_id):
    course_id = course_id
    lesson = models.Lesson.objects.get(lesson_id=lesson_id)
    category = get_language()

    #editing lesson
    if request.method == 'POST':
        try:
            lesson.lesson_name = request.POST['lesson_name']
            lesson_video = request.POST['lesson_video']
            # 擷取youtube id
            try:
                if 'youtu.be/' in lesson_video:
                    temp = lesson_video.split('be/')
                    url = temp[1]
                else:
                    temp = lesson_video.split('v=')
                    url = temp[1]
                    temp = url.split('&')
                    url = temp[0]
            except Exception as e:
                url = ''
            lesson.lesson_video = url
            lesson.lesson_content = request.POST['text-editor']
            lesson.homework_title = request.POST['homework_title']
            lesson.homework_description = request.POST['homework_description']
            if request.POST['if_compiler'] == 'False':
                lesson.if_compiler = False
            else:
                lesson.if_compiler = True
        
        
            homework_file = request.POST['filepond']
            if homework_file != '':
                arr_json = json.loads(homework_file)
                file_data = arr_json['data']
                file_name = arr_json['name']
                if file_name not in str(lesson.homework_attachment):
                    file_data = ContentFile(base64.b64decode(file_data))  
                    lesson.homework_attachment.save(file_name, file_data, save=True)
            else:
                if lesson.homework_attachment != None:
                    lesson.homework_attachment.delete()
            
            lesson.save()

            messages.add_message(request, messages.INFO, '編輯成功！')
            return HttpResponseRedirect('/course/edit/'+str(course_id)+'/')

        except Exception as e:
            messages.add_message(request, messages.ERROR, '編輯失敗！') 

    # showing editing page
    return render(request,'edit-lesson.html',locals())

# showing lesson page
def lesson_page(request,lesson_id,lesson_index):
    lesson = models.Lesson.objects.get(lesson_id=lesson_id)
    course_id = lesson.course.course_id
    is_teacher = False
    category = get_language()

    course = models.Course.objects.get(course_id=course_id)
    user_course = models.UserCourse.objects.filter(course=course,user=request.user).count()
    # if the user is the teacher or he has registered the course
    if user_course > 0 or course.teacher.email == request.user.email:
        lesson_index = lesson_index
        lesson_id = lesson_id
        all_lesson = models.Lesson.objects.filter(course=course_id).order_by('created_at')

        questions = models.Question.objects.filter(lesson=lesson).order_by('-created_at').values('question_id', 'questioner__name',
        'question_content','created_at','questioner__pic')   
        for question in questions:
            answer = models.Answer.objects.filter(question=question['question_id']).values('answer_id', 'answer_content',
            'answerer__name','created_at','answerer__pic')
            question['answer'] = list(answer)  # list()把QuerySet變成list


        all_questions = list(questions) 
        note = models.Note.objects.filter(lesson=lesson,student=request.user).first()
        note_all = models.Note.objects.filter(lesson=lesson).exclude(if_share=False)


        if course.teacher.email == request.user.email:
            is_teacher = True
            #all_homework = models.Homework.objects.filter(lesson=lesson)
            students =  models.UserCourse.objects.filter(course=course).values('user__id','user__name')
            for student in students:
                homework = models.Homework.objects.filter(lesson=lesson,student=student['user__id'])
                student['homework'] = list(homework)
            all_homework = list(students) 

        else:
            all_homework = models.Homework.objects.filter(lesson=lesson).exclude(if_share=False)
            homework = models.Homework.objects.filter(lesson=lesson,student=request.user).first()

        
        compiler_url = None
        if lesson.if_compiler:
            compiler_url = lesson.course.category.complier_url



        tab = "index"

        return render(request,'lesson.html',locals())
    else:
        messages.add_message(request, messages.ERROR, '請先註冊課程') 
        return HttpResponseRedirect('/course/'+str(course_id)+'/')


    
# lesson page 
def lesson_tab(request):
    if request.method == 'POST':
        tab = request.POST['tab']
        lesson_id = request.POST['lesson_id']
        lesson = models.Lesson.objects.get(lesson_id=lesson_id)
        if tab == "index":
            data = {}
            return JsonResponse(data,safe=False)

        if tab == 'homework':
            #lesson = models.Lesson.objects.filter(lesson_id=lesson_id)
            #data = serializers.serialize("json",lesson)
            data = {}

            return JsonResponse(data,safe=False)

        if tab == "qa":
            data = {}
            return JsonResponse(data,safe=False)

        if tab == "note":
            data = {}

            return JsonResponse(data,safe=False)

# lesson comment
def comment(request):
    if request.method == 'POST':
        question = request.POST['question']
        lesson_id = request.POST['lesson_id']
        user = request.user

        lesson = models.Lesson.objects.get(lesson_id=lesson_id)

        model_question = models.Question.objects.create(
            lesson=lesson,
            question_content=question,
            questioner=user,
        )

        model_question.save()


        questions = models.Question.objects.filter(lesson=lesson).order_by('-created_at').values('question_id', 'questioner__name','lesson__lesson_id',
        'question_content','created_at','questioner__pic')   
        for question in questions:
            answer = models.Answer.objects.filter(question=question['question_id']).values('answer_id', 'answer_content',
            'answerer__name','created_at','answerer__pic')
            question['answer'] = list(answer)  # list()把QuerySet變成list

        data = list(questions) 
        return JsonResponse(data, safe=False) 

# reply comment
def reply(request):
    if request.method =='POST':
        answer = request.POST['answer']
        question_id = request.POST['question_id']
        question = models.Question.objects.get(question_id=question_id)
        user = request.user
        lesson = models.Lesson.objects.get(lesson_id=question.lesson.lesson_id)

        answer = models.Answer.objects.create(
            question=question,
            answer_content=answer,
            answerer=user,
        )

        answer.save()

        questions = models.Question.objects.filter(lesson=lesson).order_by('-created_at').values('question_id', 'questioner__name','lesson__lesson_id',
        'question_content','created_at','questioner__pic')   
        for question in questions:
            answer = models.Answer.objects.filter(question=question['question_id']).values('answer_id', 'answer_content',
            'answerer__name','created_at','answerer__pic')
            question['answer'] = list(answer)  # list()把QuerySet變成list


        data = list(questions) 
        return JsonResponse(data,safe=False)
# register course
def register(request,course_id):
    try:
        course_id = course_id

        course = models.Course.objects.get(course_id=course_id)
        user_course = models.UserCourse.objects.update_or_create(
            user=request.user,
            course=course,
            defaults={'user': request.user},
        )

        student_count = models.UserCourse.objects.filter(course=course).count()
        messages.add_message(request, messages.INFO, '註冊成功！')

        
    except Exception as e:
        messages.add_message(request, messages.ERROR, '編輯失敗！')
    
    return HttpResponseRedirect('/course/'+str(course_id))

# upload homework in lesson page
def upload_homework(request):
    #try:
        homework = request.POST['file']
        lesson_id = request.POST['lesson_id']
        homework_url = request.POST['homework_url']
        if_share = strtobool(request.POST['if_share'])
        lesson = models.Lesson.objects.get(lesson_id=lesson_id)

        model = models.Homework.objects.filter(lesson=lesson_id,student=request.user.id).first()
        if model == None:
            hw = models.Homework.objects.create(
                lesson=lesson,
                student=request.user,
                homework_url = homework_url,
                if_share=if_share,
            )
            hw.save()

            if homework != '':
                arr_json = json.loads(homework)
                file_data = arr_json['data']
                file_name = arr_json['name']
                file_data = ContentFile(base64.b64decode(file_data))  
                             
                hw.homework.save(file_name, file_data, save=True)
                hw.save()
               

        else:
            if homework != '':
                arr_json = json.loads(homework)
                file_data = arr_json['data']
                file_name = arr_json['name']
                file_data = ContentFile(base64.b64decode(file_data))  
                model.homework.save(file_name, file_data, save=True)
                model.save()

            model.homework_url = homework_url
            model.if_share = if_share
            model.save()

    

        data = {}
        return JsonResponse(data,safe=False)
    #except Exception as e:
        #pass

def upload_pic(request):
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
        course_id = request.POST['course_id']
        models.Course.objects.filter(course_id=course_id).update(course_pic=pic_url)
        data = {}
        return JsonResponse(data,safe=False)
        
    except Exception as e:
        pass

def update_note(request):
    #try:
    lesson_id = request.POST['lesson_id']
    if_share = strtobool(request.POST['if_share'])
    lesson = models.Lesson.objects.get(lesson_id=lesson_id)


    if 'note' in request.POST:
        note = request.POST['note']
        models.Note.objects.update_or_create(
            lesson=lesson, student=request.user,
            defaults={'note': note,'if_share':if_share},
        )
    else:
        models.Note.objects.update_or_create(
            lesson=lesson, student=request.user,
            defaults={'if_share':if_share},
        )
    data = {}
    return JsonResponse(data,safe=False)
        
    #except Exception as e:
        #pass

def browse_note(request):
    note_id = request.POST['note_id']
    note = models.Note.objects.filter(id=note_id).values('student__pic','student__name','note') 
      

    data = list(note) 
    return JsonResponse(data, safe=False) 

def review(request):
    rating = request.POST['rating']
    review = request.POST['review']
    course_id = request.POST['course_id']
    if int(rating) == 0:
        #messages.add_message(request, messages.WARNING, '請評分！')
        messages.error(request, '請評分！')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])   

    course = models.Course.objects.get(course_id=course_id)
    reviewer = User.objects.get(email=request.user.email) 
    model_review = models.Review.objects.create(
            course=course,
            review=review,
            rating=int(rating),
            reviewer=reviewer,
        )

    messages.add_message(request, messages.INFO, '已評論')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])  
    
def download_homework(request):
    homework_id = request.GET['id']
    homework = models.Homework.objects.get(id=homework_id)

    s3= boto3.client('s3', 
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID, 
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, 
        region_name=settings.AWS_S3_REGION_NAME
    )
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    url = s3.generate_presigned_url('get_object', Params = {'Bucket': bucket_name, 'Key': homework.homework.name}, ExpiresIn = 100)



    request = requests.get(url, stream=True)

    # Was the request OK?
    if request.status_code != requests.codes.ok:
        return HttpResponse(status=400)

    wrapper = FileWrapper(request.raw)
    content_type = request.headers['content-type']
    content_len = request.headers['content-length']

    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Length'] = content_len
    response['Content-Disposition'] = "attachment; filename="+homework.homework.name
    return response 

