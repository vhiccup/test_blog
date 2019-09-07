from django.contrib import admin
from .models import UserProfile,UserInfo

class UserprofileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth', 'phone','sex')
    list_filter = ("phone",)
    
    
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ("user",'school','company','profession','address','aboutme','photo')
    list_filter = ('school','company','profession')
    
admin.site.register(UserProfile, UserprofileAdmin)
admin.site.register(UserInfo,UserInfoAdmin)
# Register your models here.
