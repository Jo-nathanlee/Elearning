from django.shortcuts import render
from . import models
from account.models import User
from django.contrib.auth.decorators import permission_required
from django.contrib import messages

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
    all_users = User.objects.exclude(email=request.user.email)
    return render(request, 'new-group.html',locals())

def index(request):
    teacher = User.objects.get(email=request.user.email)
    groups = models.Group.objects.all().order_by('-created_at')
    return render(request, 'group-index.html',locals())