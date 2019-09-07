from django.shortcuts import render,get_object_or_404

# Create your views here.
from .models import BlogArticles
from .forms import BlogArticlePostForm
#from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse


@login_required(login_url='/account/login/')
def blog_title(request):
    blog_list = BlogArticles.objects.filter(author=request.user)
    paginator = Paginator(blog_list,4)
    page = request.GET.get('page')
    #print(page)
    try:
        current_page = paginator.page(page)
        blogs = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        blogs = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        blogs = current_page.object_list
    return render(request,'blog/blog/titles.html',{'blogs':blogs,"page":current_page})



def blog_article(request,article_id):
    #article = BlogArticles.objects.get(id=article_id)
    article =get_object_or_404(BlogArticles,id=article_id)
    pub = article.publish
    return render(request,'blog/blog/content.html',{"article":article,'publish':pub})

@login_required(login_url='/account/login/')
@csrf_exempt
def blog_article_post(request):
    if request.method == "POST":
        blog_article_post_form = BlogArticlePostForm(data=request.POST)
        if blog_article_post_form.is_valid():
            cd = blog_article_post_form.cleaned_data
            try:
                new_blog_article = blog_article_post_form.save(commit=False)
                new_blog_article.author = request.user
                new_blog_article.save()
                messages.success(request,'文章发布成功')
                return HttpResponseRedirect(reverse("blog:blog_title"))
                #return HttpResponse('1')
            except:
                messages.error(request,'对不起，文章发布失败')
                return HttpResponseRedirect(reverse("blog:blog_title"))
                #return HttpResponse('2')
        else:
            messages.error(request,'对不起，文章格式输入错误')
            return HttpResponseRedirect(reverse("blog:blog_title"))
            #return HttpResponse('3')
    if request.method == "GET":
        blog_article_post_form = BlogArticlePostForm()
        return render(request, "blog/blog/blog_post.html",{"blog_article_post_form":blog_article_post_form})
