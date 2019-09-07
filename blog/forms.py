# -*- coding: utf-8 -*-
# 'author':'hxy'


from django import forms
from django.contrib.auth.models import User
from .models import BlogArticles


class BlogArticlePostForm(forms.ModelForm):
    class Meta:
        model = BlogArticles
        fields = ("title","body")
    
      