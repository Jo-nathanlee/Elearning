from django.shortcuts import render
from . import models
from course.models import Course
from account.models import User
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
import base64
import json
from django.core.files.base import ContentFile
import boto3
import requests
from wsgiref.util import FileWrapper
from django.http import Http404, HttpResponse
from django.conf import settings

# Create your views here.
# create a new group
@permission_required('course.can_access', raise_exception = True )
def new(request,course_id):
    # creating
    if request.method == "POST":
        try:
            members = request.POST.getlist('members')
            teacher = User.objects.get(email=request.user.email) 
            course = Course.objects.get(course_id=course_id)
            course_group = models.Group.objects.filter(course=course)
            group_num = 1
            if course_group.count() > 0:
                group_num = (course_group.count())+1

            new_group = models.Group.objects.create(
                teacher=teacher,
                course=course,
                group_num=group_num,
            )
            new_group.save()
            for member_id in members:
                new_group.member.add(int(member_id))

            messages.add_message(request, messages.INFO, '建立成功！')
            return HttpResponseRedirect('/group/'+str(course_id))
        except Exception as e:
            messages.add_message(request, messages.ERROR, '建立失敗！')

        

    #showing creating page
    courses = Course.objects.filter(course_id=course_id).distinct('teacher')
    groups = models.Group.objects.all()
    all_users = User.objects.exclude(id__in=[course.teacher.id for course in courses])
    return render(request, 'new-group.html',locals())

@permission_required('course.can_access', raise_exception = True )
def edit(request,group_id):
    group = models.Group.objects.get(id=group_id)
    if request.method == "POST":
        try:
            members = request.POST.getlist('members')
            
            group.member.clear()
            for member_id in members:
                group.member.add(int(member_id))

            messages.add_message(request, messages.INFO, '編輯成功！')
            return HttpResponseRedirect('/group/'+str(group.course.course_id))
        except Exception as e:
            messages.add_message(request, messages.ERROR, '編輯失敗！')
    group_members = group.member.all()
    #showing edit page
    courses = Course.objects.distinct('teacher')
    groups = models.Group.objects.all()
    other_users = User.objects.exclude(id__in=group_members).exclude(id__in=[course.teacher.id for course in courses])
    return render(request, 'edit-group.html',locals())

@permission_required('course.can_access', raise_exception = True )
def delete(request,group_id):
    try:
        group = models.Group.objects.get(id=group_id)
        group.delete()
        messages.add_message(request, messages.INFO, '刪除成功！')
    except Exception as e:
        messages.add_message(request, messages.ERROR, '刪除失敗！')
    return HttpResponseRedirect('/group/'+str(group.course.course_id))

@permission_required('course.can_access', raise_exception = True )
def admin(request,course_id):
    teacher = User.objects.get(email=request.user.email)
    course = Course.objects.get(course_id=course_id)
    groups = models.Group.objects.filter(course=course).order_by('-created_at')
    return render(request, 'group-admin.html',locals())

def forum(request,group_id):
    group_id=group_id
    group = models.Group.objects.get(id=group_id)
    posts = models.GroupPost.objects.filter(group=group_id)

    return render(request, 'group-forum.html',locals())

def mygroup(request,course_id):
    course = Course.objects.get(course_id=course_id)
    course_group = models.Group.objects.filter(course=course)
    mygroup = course_group.filter(member__email=request.user.email)

    return render(request, 'mygroup.html',locals())

def new_post(request,group_id):
    # creating
    if request.method == "POST":
        #try:
            title = request.POST['title']
            content = request.POST['text-editor']
            creator_id = request.user.id

            model_post = models.GroupPost.objects.create(
                title=title,
                content=content,
                creator_id=creator_id,
                group_id=group_id,
            )
            model_post.save()

            messages.add_message(request, messages.INFO, '新增成功！')
            return HttpResponseRedirect('/group/forum/'+str(group_id) )
        #except Exception as e:
            #messages.add_message(request, messages.ERROR, '新增失敗！')

    #showing creating page
    return render(request, 'edit-post.html',locals())

def edit_post(request,post_id):
    post = models.GroupPost.objects.get(id=post_id)
     # creating
    if request.method == "POST":
        try:
            title = request.POST['title']
            content = request.POST['text-editor']

            post.title = title
            post.content = content
            post.save()

            messages.add_message(request, messages.INFO, '編輯成功！')
            return HttpResponseRedirect('/group/post/{{ post_id }}')
        except Exception as e:
            messages.add_message(request, messages.ERROR, '編輯失敗！')

    #showing creating page
    return render(request, 'edit-post.html',locals())

def delete_post(request,post_id):
    try:
        post = models.GroupPost.objects.get(id=post_id)
        post.delete()
        messages.add_message(request, messages.INFO, '刪除成功！')
    except Exception as e:
        messages.add_message(request, messages.ERROR, '刪除失敗！')
    return HttpResponseRedirect('/group/forum/{{ group_id }}')

def post(request,post_id):
    post = models.GroupPost.objects.get(id=post_id)
    group_id = post.group.id
    group_num = post.group.group_num
    comments = models.GroupComment.objects.filter(post_id=post_id)

    return render(request, 'post.html',locals())

def comment(request):
    if request.method == 'POST':
        comment = request.POST['comment']
        post_id = request.POST['post_id']

        model_comment = models.GroupComment.objects.create(
            post_id=post_id,
            content=comment,
            creator=request.user,
        )

        model_comment.save()


        comments = models.GroupComment.objects.filter(post=post_id).order_by('-created_at').values('id', 'creator__name',
        'content','created_at','creator__pic')   

        data = list(comments) 
        return JsonResponse(data, safe=False) 

def upload_project(request):
    try:
        project = request.POST['file']
        group_id = request.POST['group_id']
        project_url = request.POST['project_url']

        group = models.Group.objects.get(id=group_id)
        if project != '':
            arr_json = json.loads(project)
            file_data = arr_json['data']
            file_name = arr_json['name']
            file_data = ContentFile(base64.b64decode(file_data)) 

            group.project.save(file_name, file_data, save=True)
            group.save()

        group.project_url = project_url
        group.save()

        data = {}
        return JsonResponse(data,safe=False)
    except Exception as e:
        pass

def download_project(request):
    group_id = request.GET['id']
    group = models.Group.objects.get(id=group_id)

    s3= boto3.client('s3', 
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID, 
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, 
        region_name=settings.AWS_S3_REGION_NAME
    )
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    url = s3.generate_presigned_url('get_object', Params = {'Bucket': bucket_name, 'Key': group.project.name}, ExpiresIn = 100)



    request = requests.get(url, stream=True)

    # Was the request OK?
    if request.status_code != requests.codes.ok:
        return HttpResponse(status=400)

    wrapper = FileWrapper(request.raw)
    content_type = request.headers['content-type']
    content_len = request.headers['content-length']

    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Length'] = content_len
    response['Content-Disposition'] = "attachment; filename="+group.project.name
    return response 
