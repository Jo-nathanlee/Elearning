from django.shortcuts import render
from . import models
from account.models import User
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect

# Create your views here.
# create a new group
@permission_required('course.can_access', raise_exception = True )
def new(request):
    # creating
    if request.method == "POST":
        try:
            members = request.POST.getlist('members')
            teacher = User.objects.get(email=request.user.email) 

            new_group = models.Group.objects.create(
                teacher=teacher,
            )
            new_group.save()
            for member_id in members:
                new_group.member.add(int(member_id))

            messages.add_message(request, messages.INFO, '建立成功！')
            return HttpResponseRedirect('/group/')
        except Exception as e:
            messages.add_message(request, messages.ERROR, '建立失敗！')

        

    #showing creating page
    all_users = User.objects.exclude(email='test@gmail.com')
    return render(request, 'new-group.html',locals())

@permission_required('course.can_access', raise_exception = True )
def edit(request,group_id):
    group = models.Group.objects.get(id=group_id)
    if request.method == "POST":
        try:
            members = request.POST.getlist('members')
            
            group.member_set.clear()
            for member_id in members:
                group.member.add(int(member_id))

            messages.add_message(request, messages.INFO, '編輯成功！')
            return HttpResponseRedirect('/group/')
        except Exception as e:
            messages.add_message(request, messages.ERROR, '編輯失敗！')
    group_members = group.member.all()
    #showing edit page
    other_users = User.objects.exclude(id__in=group_members).exclude(email='test@gmail.com')
    
    return render(request, 'edit-group.html',locals())

@permission_required('course.can_access', raise_exception = True )
def delete(request,group_id):
    try:
        group = models.Group.objects.get(id=group_id)
        group.delete()
        messages.add_message(request, messages.INFO, '刪除成功！')
    except Exception as e:
        messages.add_message(request, messages.ERROR, '刪除失敗！')
    return HttpResponseRedirect('/group/')

@permission_required('course.can_access', raise_exception = True )
def index(request):
    teacher = User.objects.get(email=request.user.email)
    groups = models.Group.objects.all().order_by('-created_at')
    return render(request, 'group-index.html',locals())

def forum(request,group_id):
    group_id=group_id
    posts = models.GroupPost.objects.filter(group=group_id)

    return render(request, 'group-forum.html',locals())

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
            return HttpResponseRedirect('/group/'+group_id )
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
    return HttpResponseRedirect('/group/{{ group_id }}')

def post(request,post_id):
    post = models.GroupPost.objects.get(id=post_id)
    group_id = post.group.id
    comments = models.GroupComment.objects.filter(post_id=post_id)

    return render(request, 'post.html',locals())

def comment(request,post_id):
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