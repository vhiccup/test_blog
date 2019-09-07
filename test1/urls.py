"""test1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('blog/',include('blog.urls',namespace='blog',app_name='blog')),
    #path('blog/', include('blog.urls')),
    #path('blog/', include('blog.urls', namespace='blog')),
    #path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    #re_path(r'^blog/',include('blog.urls'))
    path('account/',include('account.urls', namespace='account')),
    path('pwd-reset/',include("password_reset.urls",namespace='pwd_reset')),
    path('article/', include("article.urls",namespace='article')),
    path('',TemplateView.as_view(template_name="home.html"),name='home'),
    path('favicon.ico',RedirectView.as_view(url='/static/images/favicon.ico'),name='icon'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
