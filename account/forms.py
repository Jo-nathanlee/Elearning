from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class AccountForm(forms.Form):
    name = forms.CharField(max_length=255,required=True)
    email = forms.EmailField(max_length=255,required=True)
    password = forms.CharField(max_length=255,required=True)

# class UserCreationForm(UserCreationForm):

#     class Meta:
#         model = User
#         fields = ('email','password')

# class UserChangeForm(UserChangeForm):

#     class Meta:
#         model = User
#         fields = ('email', 'password', 'birthday', 'sex','pic_url','language_learnt')

