from django.urls import path
from . import views

urlpatterns = [
    # Home page listing all articles
    path('', views.home, name='home'),

    # Page for a specific category, using the category's slug
    path('category/<slug:category_slug>/', views.category_view, name='category_view'),

    # Page for a specific tag, using the tag's slug
    path('tag/<slug:tag_slug>/', views.tag_view, name='tag_view'),

    # Search results page
    path('search/', views.search_view, name='search_view'),

    # Detail page for a single article, using the article's slug
    path('article/<slug:slug>/', views.article_detail_view, name='article_detail_view'),
]