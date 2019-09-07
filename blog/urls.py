# -*- coding: utf-8 -*-
# 'author':'hxy'


from django.urls import path
from blog import views


app_name='blog'
urlpatterns = [
    path('', views.blog_title, name='blog_title'),
    path('<int:article_id>/',views.blog_article,name="blog_detail"),
    path('blogpost/',views.blog_article_post,name="blog_post"),
]
