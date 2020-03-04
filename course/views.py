from django.shortcuts import render
from . import models
from account.models import User
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
# Create your views here.
def new_course(request):
    if request.method == "POST":
        course_name = request.POST['course_name']
        category = request.POST['category']
        course_introduction = request.POST['course_introduction']

        picture = request.POST['picture']
        arr_json = json.loads(picture)
        json_data = arr_json['data']
        file_name = arr_json['name']
        pic_data = ContentFile(base64.b64decode(json_data))  


        #foreign key
        model_category = models.Category.objects.get(category_name=category)  
        teacher = User.objects.get(email=request.user.email) 



        model_course = models.Course.objects.create(
            course_name=course_name,
            category=model_category,
            course_introduction=course_introduction,
            teacher=teacher
        )
        model_course.course_pic.save(file_name, pic_data, save=True)
        model_course.save()

        messages.add_message(request, messages.INFO, '新增成功！')

        return HttpResponseRedirect('/course/edit/'+str(model_course.course_id)+'/')


    category = models.Category.objects.all()   

    return render(request, 'new-course.html',locals())

def course_index(request):
    all_course = models.Course.objects.all().order_by('-created_at')

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

    category = models.Category.objects.all()   
    latest_course = paginator.page(1)

    return render(request,'courses.html',locals())

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

    latest_course = paginator.page(1)
    category = models.Category.objects.all()

    return render(request,'user-courses.html',locals())

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
    category = models.Category.objects.all()   

    return render(request,'courses.html',locals())

def course_page(request,course_id):
    course_id = course_id
    course = models.Course.objects.get(course_id=course_id)
    teacher = User.objects.get(email=course.teacher)
    teacher_course_count = models.Course.objects.filter(teacher=course.teacher).count()
    lesson = models.Lesson.objects.filter(course_id=course)

    return render(request,'single-course.html',locals())

def course_edit(request,course_id):
    course = models.Course.objects.get(course_id=course_id)
    category = models.Category.objects.all()   
    lesson = models.Lesson.objects.filter(course_id=course)

    if request.method == "POST":
        category_name = request.POST['category']
        model_category = models.Category.objects.get(category_name=category_name)  
        course.course_name = request.POST['course_name']
        course.category = model_category
        course.course_introduction = request.POST['course_introduction']

        picture = request.POST['picture']
        arr_json = json.loads(picture)
        json_data = arr_json['data']
        file_name = arr_json['name']
        pic_data = ContentFile(base64.b64decode(json_data))  

        course.course_pic.save(file_name, pic_data, save=True)
        course.save()

        messages.add_message(request, messages.INFO, '編輯成功！')

    return render(request,'edit-course.html',locals())

def course_delete(request,course_id):

    course = models.Course.objects.get(course_id=course_id)
    course.delete()
    messages.add_message(request, messages.INFO, '刪除成功！')

    return HttpResponseRedirect('/index/teacher')

def new_lesson(request,course_id):
    course_id = course_id
    if request.method == 'POST':
        lesson_name = request.POST['lesson_name']
        lesson_video = request.POST['lesson_video']
        # 擷取youtube id
        temp = lesson_video.split('watch?v=')
        lesson_video = temp[1]
        lesson_content = request.POST['text-editor']
        homework_title = request.POST['homework_title']
        homework_description = request.POST['homework_description']

        

        course_id = models.Course.objects.get(course_id = course_id)

        lesson = models.Lesson.objects.create(
            course_id=course_id,
            lesson_name=lesson_name,
            lesson_video=lesson_video,
            lesson_content=lesson_content,
            homework_title=homework_title,
            homework_description=homework_description
        )
        try:
            homework_file = request.POST['filepond']

            arr_json = json.loads(homework_file)
            file_data = arr_json['data']
            file_name = arr_json['name']
            file_data = ContentFile(base64.b64decode(file_data))  
            lesson.homework_attachment.save(file_name, file_data, save=True)
        except Exception as e:
            pass
       
        lesson.save()

        messages.add_message(request, messages.INFO, '新增成功！')
    return render(request,'edit-lesson.html',locals())

def edit_lesson(request,course_id,lesson_id):
    course_id = course_id
    lesson = models.Lesson.objects.get(lesson_id=lesson_id)

    if request.method == 'POST':
        lesson.lesson_name = request.POST['lesson_name']
        lesson.lesson_video = request.POST['lesson_video']
        # 擷取youtube id
        temp = lesson_video.split('watch?v=')
        lesson.lesson_video = temp[1]
        lesson.lesson_content = request.POST['text-editor']
        lesson.homework_title = request.POST['homework_title']
        lesson.homework_description = request.POST['homework_description']
        
        try:
            homework_file = request.POST['filepond']

            arr_json = json.loads(homework_file)
            file_data = arr_json['data']
            file_name = arr_json['name']
            file_data = ContentFile(base64.b64decode(file_data))  
            lesson.homework_attachment.save(file_name, file_data, save=True)
        except Exception as e:
            pass

        lesson.save()

        messages.add_message(request, messages.INFO, '編輯成功！')


    return render(request,'edit-lesson.html',locals())

def lesson_page(request,lesson_id,lesson_index):
    lesson = models.Lesson.objects.get(lesson_id=lesson_id)
    lesson_index = lesson_index
    course_id = lesson.course_id.course_id
    lesson_id = lesson_id
    all_lesson = models.Lesson.objects.filter(course_id=course_id).order_by('created_at')

    questions = models.Question.objects.filter(lesson_id=lesson).order_by('-created_at').values('question_id', 'questioner__name','lesson_id_id',
    'question_content','created_at','questioner__pic')   
    for question in questions:
        answer = models.Answer.objects.filter(question=question['question_id']).values('answer_id', 'answer_content',
        'answerer__name','created_at','answerer__pic')
        question['answer'] = list(answer)  # list()把QuerySet變成list


    all_questions = list(questions) 
    homework = models.Homework.objects.filter(lesson_id=lesson_id,student=request.user).first()

    tab = "index"

    return render(request,'lesson.html',locals())

def index_tab(request):
    if request.method == 'POST':
        tab = request.POST['tab']
        lesson_id = request.POST['lesson_id']
        if tab == "index":
            data = {}
            return JsonResponse(data,safe=False)

        if tab == 'homework':
            lesson = models.Lesson.objects.filter(lesson_id=lesson_id)
            data = serializers.serialize("json",lesson)

            return JsonResponse(data,safe=False)

        if tab == "qa":
            data = {}
            return JsonResponse(data,safe=False)


def comment(request):
    if request.method == 'POST':
        question = request.POST['question']
        lesson_id = request.POST['lesson_id']
        user = request.user

        lesson = models.Lesson.objects.get(lesson_id=lesson_id)

        model_question = models.Question.objects.create(
            lesson_id=lesson,
            question_content=question,
            questioner=user,
        )

        model_question.save()


        questions = models.Question.objects.filter(lesson_id=lesson).order_by('-created_at').values('question_id', 'questioner__name','lesson_id_id',
        'question_content','created_at','questioner__pic')   
        for question in questions:
            answer = models.Answer.objects.filter(question=question['question_id']).values('answer_id', 'answer_content',
            'answerer__name','created_at','answerer__pic')
            question['answer'] = list(answer)  # list()把QuerySet變成list

        data = list(questions) 
        return JsonResponse(data, safe=False) 

def reply(request):
    if request.method =='POST':
        answer = request.POST['answer']
        question_id = request.POST['question_id']
        question = models.Question.objects.get(question_id=question_id)
        user = request.user

        answer = models.Answer.objects.create(
            question=question,
            answer_content=answer,
            answerer=user,
        )

        answer.save()

        questions = models.Question.objects.filter(question_id=question_id).values('question_id', 'questioner__name','lesson_id_id',
        'question_content','created_at','questioner__pic')   
        for question in questions:
            answer = models.Answer.objects.filter(question=question['question_id']).values('answer_id', 'answer_content',
            'answerer__name','created_at','answerer__pic')
            question['answer'] = list(answer)  # list()把QuerySet變成list


        data = list(questions) 
        return JsonResponse(data,safe=False)

def register(request):
    if request.method =='POST':
        try:
            course_id = request.POST['course_id']

            course = models.Course.objects.get(course_id=course_id)
            user_course = models.UserCourse.objects.update_or_create(
                user=request.user,
                course=course,
                defaults={'user': request.user},
            )

            
            data = {'success':True}
            messages.add_message(request, messages.INFO, '註冊成功！')
        except Exception as e:
            data = {'success':False}
            messages.add_message(request, messages.ERROR, '註冊失敗！')
        return JsonResponse(data,safe=False)

def upload_homework(request):
    homework = request.POST['file']
    lesson_id = request.POST['lesson_id']


    arr_json = json.loads(homework)
    file_data = arr_json['data']
    file_name = arr_json['name']
    file_data = ContentFile(base64.b64decode(file_data))  

    lesson = models.Lesson.objects.get(lesson_id=lesson_id)
    student = User.objects.get(email=request.user.email) 

    
    model = models.Homework.objects.filter(lesson_id=lesson,student=student).first()
    if model == None:
        hw = models.Homework.objects.create(
            lesson_id=lesson,
            student=student,
        )
        hw.homework.save(file_name, file_data, save=True)
        hw.save()
    else:
        model.homework.save(file_name, file_data, save=True)
        model.save()

   

    data = {}
    return JsonResponse(data,safe=False)