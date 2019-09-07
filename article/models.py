from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from slugify import slugify
from ckeditor_uploader.fields import RichTextUploadingField


class ArticleColumn(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE,related_name="article_column")
    column = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.column

class ArticlePost(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="article")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500)
    column = models.ForeignKey(ArticleColumn,on_delete=models.CASCADE,related_name="article_column")
    body = RichTextUploadingField(blank=True,null=True,verbose_name="内容")
    user_like=models.ManyToManyField(User,related_name='articles_likes',blank=True)
    user_dislike=models.ManyToManyField(User,related_name='articles_dislikes',blank=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-updated',)
        index_together=(('id','slug'),)
    
    def __str__(self):
        return self.title
    
    def save(self,*args,**kargs):
        self.slug = slugify(self.title)
        super(ArticlePost,self).save(*args,**kargs)
    
    def get_absolute_url(self):
        return reverse("article:article_detail",args=[self.id,self.slug])
    
    
    def get_url_path(self):
        return reverse("article:article_content",args=[self.id,self.slug])
        


class  Comment(models.Model):
    article=models.ForeignKey(ArticlePost,on_delete=models.CASCADE,related_name="comments")
    commentor=models.CharField(max_length=50)
    body = RichTextUploadingField(config_name='comment',blank=True,null=True,verbose_name="评论")
    created= models.DateField(auto_now_add=True)
    
    class Meta:
        ordering=('-created',)
    def __str__(self):
        return "Comment by {0} on {1}".format(self.commentor,self.article)
    
# Create your models here.


