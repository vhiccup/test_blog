from django.contrib import admin
from .models import ArticleColumn,ArticlePost

class ArticleColumnAdmin(admin.ModelAdmin):
    list_display = ('column','created','user')
    list_filter = ('column',)


class ArticlePostAdmin(admin.ModelAdmin):
    list_display = ('author','title')
    filter_horizontal = ('user_like','user_dislike')
    list_filter = ('author',)
admin.site.register(ArticleColumn,ArticleColumnAdmin)
admin.site.register(ArticlePost,ArticlePostAdmin)


# Register your models here.
