from django.contrib import admin
from .models import *
admin.site.site_title ="Admin Forum Baca"
admin.site.site_header ="Admin Forum Baca"
admin.sites.AdminSite.site_header ="Admin Forum Baca"
# Register your models here.
class PostinganAdmin(admin.ModelAdmin):
    list_display = ('judul', 'penulis', 'tanggal_dibuat', 'gambar', )
    prepopulated_fields = {"slug":("judul","penulis")}
    search_fields=('judul','penulis__username')
class QuotesAdmin(admin.ModelAdmin):
    list_display = ('quotes', 'author', 'show', )
    list_editable = ('show',)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('posting','user')
    
admin.site.register(Quotes, QuotesAdmin)

admin.site.register(Postingan,PostinganAdmin)
admin.site.register(Komentar)