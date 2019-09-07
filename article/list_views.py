from django.shortcuts import render ,get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from .models import ArticleColumn, ArticlePost,Comment
from .forms import CommentForm
from django.contrib.auth.models import User
from django.contrib import messages
import redis
from django.conf import settings

#r=redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)
r = redis.StrictRedis(host="localhost",port=6379,db=0)

def article_titles(request,username=None):
    if username:
        user_author=User.objects.get(username=username)
        articles_title = ArticlePost.objects.filter(author=user_author)
        try:
            authorinfo=user_author.userinfo
        except:
            authorinfo=None
    else:
        articles_title = ArticlePost.objects.all() 
    paginator = Paginator(articles_title, 3) 
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list 
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list 
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages) 
        articles = current_page.object_list
    if username:
        return render(request, "article/list/author_articles.html",{"articles":articles,"page":current_page,"authorinfo":authorinfo,"user_author":user_author})
    else:
        return render(request, "article/list/article_titles.html", {"articles":articles, "page": current_page})


def article_details(request,id,slug):
    article = get_object_or_404(ArticlePost,id=id,slug=slug)
    total_views=r.incr("article:{}:views".format(article.id))
    r.zincrby('article_ranking',article.id, 1)
    article_ranking=r.zrange('article_ranking',0,-1,desc=True)[:10] 
    article_ranking_ids = [int(id) for id in article_ranking]
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))
    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))
    comments=article.comments.all()
    if request.method=="POST":
        comment_form = CommentForm(data=request.POST)
        try:
            if comment_form.is_valid():
                new_comment=comment_form.save(commit= False)
                new_comment.article=article
                new_comment.commentor=request.user
                new_comment.save()
                messages.success(request,'评论成功')
        except:
            messages.error(request,'评论失败')
    else:
        comment_form=CommentForm()
    return render(request,"article/list/article_detail.html",{"article":article,"total_views":total_views,"most_viewed":most_viewed,"comments":comments,"comment_form":comment_form})

