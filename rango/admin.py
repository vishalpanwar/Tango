from django.contrib import admin
from rango.models import Category, Page, UserProfile

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    class Meta:
        Category

class PageAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'category')
    class Meta:
        Page

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)