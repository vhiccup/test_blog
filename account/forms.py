# -*- coding: utf-8 -*-
# 'author':'hxy'


from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, UserInfo


class LoginForm(forms.Form):
    username = forms.CharField(help_text='用户名长度1-16位，由字母、数字、下划线组成')
    password = forms.CharField(widget =forms.PasswordInput)

class RegidtrationFrom(forms.ModelForm):
    password = forms.CharField(label = "password",help_text='用户名长度1-16位，由字母、数字、下划线组成',widget=forms.PasswordInput,)
    password2 = forms.CharField(label = "Confirm Password", widget = forms.PasswordInput)
    
    class Meta:
        model=User
        fields = ("username","email")
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password']!=cd['password2']:
            raise forms.ValidationError("passwords do not match.")
        return cd['password2']

class UserprofileForm(forms.ModelForm):
    class Meta:
        model= UserProfile
        fields = ("phone","birth","sex")
    
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ("school","company","profession","address","aboutme","photo")
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)