from django.contrib import admin
from .models import Category, Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'status', 'url')
    list_filter = ('status',)  # Define the list filter for the 'status' field


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)