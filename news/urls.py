# news/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:category_slug>/', views.category_view, name='category_view'),
    path('tag/<slug:tag_slug>/', views.tag_view, name='tag_view'),
    path('search/', views.search_view, name='search_view'),

    # ✅ FIXED: Changed path converter from <slug:slug> to <str:slug>
    # This allows the URL to accept Unicode characters from the slug.
    path('article/<str:slug>/', views.article_detail_view, name='article_detail_view'),

    path('add/', views.add_article_view, name='add_article'),
]
