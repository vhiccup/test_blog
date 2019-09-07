from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from slugify import slugify
# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User

class BlogArticles(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='blog_posts')
    slug = models.SlugField(max_length=500)
    
    body = RichTextUploadingField(blank=True,null=True,verbose_name="内容")
    publish = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ('-publish',)
        index_together=(('id','slug'),)
    
    def __str__(self):
        return self.title
    
    def save(self,*args,**kargs):
        self.slug = slugify(self.title)
        super(BlogArticles,self).save(*args,**kargs)
    
#    def get_absolute_url(self):
#        return reverse("article:article_detail",args=[self.id,self.slug])
#    
#    
#    def get_url_path(self):
#        return reverse("article:article_content",args=[self.id,self.slug])
        

    