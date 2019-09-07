# -*- coding: utf-8 -*-
# 'author':'hxy'


from django import forms
from django.contrib.auth.models import User
from .models import ArticleColumn, ArticlePost,Comment

class ArticleColumnForm(forms.ModelForm):
    class Meta:
        model = ArticleColumn
        fields = ("column",)

class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ("title","body")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
      