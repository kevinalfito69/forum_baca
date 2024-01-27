from django.contrib import admin
from .models import *
# Register your models here.
admin.site.login_template = 'login.html'
class userProfileAdmin(admin.ModelAdmin):
    list_display=('user',)
    
    
admin.site.register(UserProfile,userProfileAdmin)
