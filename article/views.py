from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ArticleColumn,ArticlePost
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .forms import ArticleColumnForm,ArticlePostForm
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
import redis
from django.conf import settings

#r=redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)
r = redis.StrictRedis(host="localhost",port=6379,db=0,decode_responses=True)

@login_required(login_url='/account/login/')
@csrf_exempt
def article_column(request):

    if request.method == "GET":
        columns = ArticleColumn.objects.filter(user=request.user)
        column_form=ArticleColumnForm()
        return render(request,"article/column/article_column.html/",{"columns":columns,"column_form":column_form})
    if request.method == "POST":
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user_id=request.user.id,column=column_name)
        if columns:
            return HttpResponse('2')
        else:
            ArticleColumn.objects.create(user=request.user,column=column_name)
            return HttpResponse('1')


@login_required(login_url='/account/login/')
@require_POST
@csrf_exempt
def rename_article_column(request):
    column_name = request.POST['column_name']
    column_id = request.POST['column_id']
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.column = column_name
        line.save()
        return HttpResponse('1')
    except:
        return HttpResponse('0')

@login_required(login_url='/account/login/')
@require_POST
@csrf_exempt
def del_article_column(request):
    column_id = request.POST['column_id']
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.delete()
        return HttpResponse('1')
    except:
        return HttpResponse('2')  

@login_required(login_url='/account/login/')
@csrf_exempt
def article_post(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        columnid=request.POST.get('column_id')
        print(columnid)
        print(article_post_form)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                new_article.column = ArticleColumn.objects.get(id=columnid)
                #new_article.column = request.user.article_column.get(id = request.POST['column_id'])
                new_article.save()
                messages.success(request,'发布成功')
                return HttpResponseRedirect(reverse("article:article_list"))
            except:
                messages.error(request,'发布失败')
                return HttpResponseRedirect(reverse("article:article_list"))
        else:
            messages.error(request,'发布失败')
            return HttpResponseRedirect(reverse("article:article_list"))
        
    if request.method == "GET":
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        return render(request, "article/column/article_post.html",{"article_post_form":article_post_form, "article_columns":article_columns})

@login_required(login_url='/account/login/')
def article_list(request):
    article_list = ArticlePost.objects.filter(author=request.user)
    paginator = Paginator(article_list,4)
    page = request.GET.get('page')
    #print(page)
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    return render(request, "article/column/article_list.html",{"articles":articles, "page":current_page})
       
#@login_required(login_url='/account/login/')
def article_detail(request,id,slug):
    article = get_object_or_404(ArticlePost,id=id,slug=slug)
    total_views=r.get("article:{}:views".format(article.id))
    if total_views==None:
        total_views=0

    #total_views=1
    r.zincrby('article_ranking',article.id, 1)
    article_ranking=r.zrange('article_ranking',0,-1,desc=True)[:10] 
    article_ranking_ids = [int(num) for num in article_ranking]
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))
    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))
    return render(request,"article/column/article_detail.html",{"article":article,"total_views":total_views,"most_viewed": most_viewed})

@login_required(login_url='/account/login/')
@require_POST
@csrf_exempt
def del_article(request):
    article_id = request.POST['article_id']
    try:
        article = ArticlePost.objects.get(id = article_id)
        article.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@login_required(login_url='/account/login/')
@csrf_exempt
def redit_article(request, article_id):
    if request.method == "GET":
        article_columns = request.user.article_column.all()
        article = ArticlePost.objects.get(id = article_id)
        this_article_form = ArticlePostForm(initial={"title":article.title,'body':article.body})
        this_article_column = article.column
        return render(request, "article/column/redit_article.html", {"article":article,"article_columns":article_columns, "this_article_column":this_article_column,"this_article_form":this_article_form})
    if request.method == "POST":
        redit_article = ArticlePost.objects.get(id=article_id)
        try:
            redit_article.column = request.user.article_column.get(id=request.POST['column_id'])
            redit_article.title = request.POST['title']
            redit_article.body = request.POST['body']
            redit_article.save()
            messages.success(request,'修改成功')
            return HttpResponseRedirect(reverse("article:article_list"))
        except:
            messages.error(request,'修改失败')
            return HttpResponseRedirect(reverse("article:article_list"))

@login_required(login_url='/account/login/')
@require_POST
@csrf_exempt
def like_article(request):
    article_id=request.POST.get("id")
    action = request.POST.get("action")
    try:
        article=ArticlePost.objects.get(id=article_id)
        if action=='like':
#            if request.user not in article.user_like:
#                if request.user in article.user_dislike:
#                    article.user_dislike.remove(request.user)
#                else:
            article.user_like.add(request.user)
        elif action=='dislike':
#            if request.user  not in article.user_dislike:
#                if request.user in article.user_like:
#                    article.user_like.remove(request.user)
#                else:
            article.user_dislike.add(request.user)
        return HttpResponse("1")
    except:
        return HttpResponse("0")
        
# Create your views here.
