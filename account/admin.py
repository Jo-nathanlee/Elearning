from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User

# Register your models here.


# class UserAdmin(UserAdmin):
#     add_form = UserCreationForm
#     form = UserChangeForm
#     model = User
#     list_display = ['id','username','email','password','birthday','sex','language_learnt','pic_url']

# admin.site.register(User, UserAdmin)

@admin.register(User)
class UserAdmin(UserAdmin):
    """Define admin model for custom User model with no email field."""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('name', 'department','sex','language_learnt','pic','if_teacher')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ['id','name','email','password','department','sex','language_learnt','pic','if_teacher','is_staff', 'is_active', 'is_superuser']
    search_fields = ('email','name')
    ordering = ('email',)