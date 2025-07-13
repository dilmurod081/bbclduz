# news/admin.py

from django.contrib import admin
from .models import Article, Category, Tag, Comment, Opinion

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    # ✅ FIXED: Added search_fields so ArticleAdmin can autocomplete categories.
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    # ✅ FIXED: Added search_fields so ArticleAdmin can autocomplete tags.
    search_fields = ('name',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_at', 'is_lead')
    list_filter = ('category', 'is_lead', 'published_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    # This now works because CategoryAdmin and TagAdmin have 'search_fields'.
    autocomplete_fields = ('category', 'tags')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'article', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('author', 'body')

@admin.register(Opinion)
class OpinionAdmin(admin.ModelAdmin):
    list_display = ('author', 'quote')
    search_fields = ('author', 'quote')