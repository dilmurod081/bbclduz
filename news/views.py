# news/views.py

from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
from .models import Article, Category, Tag, Opinion, Comment
from .forms import ArticleForm # Removed CategoryForm and TagForm

def _get_common_context():
    """Returns a dictionary with context data needed on almost every page."""
    return {
        'categories': Category.objects.all(),
        'popular_tags': Tag.objects.exclude(slug__exact='').order_by('-id')[:10],
        'latest_news': Article.objects.order_by('-published_at')[:5],
        'recent_comments': Comment.objects.order_by('-created_at')[:4],
    }

def home(request):
    """Displays the home page with a paginated list of all articles."""
    common_context = _get_common_context()
    article_list = Article.objects.all().order_by('-published_at')
    paginator = Paginator(article_list, 10)
    page_number = request.GET.get('page')
    articles_page = paginator.get_page(page_number)
    context = {
        **common_context,
        'page_title': 'Bosh sahifa',
        'articles': articles_page,
        'active_category': None,
    }
    return render(request, 'news/index.html', context)

def category_view(request, category_slug):
    """Displays articles for a specific category, with pagination."""
    common_context = _get_common_context()
    category = get_object_or_404(Category, slug=category_slug)
    article_list = Article.objects.filter(category=category).order_by('-published_at')
    paginator = Paginator(article_list, 10)
    page_number = request.GET.get('page')
    articles_page = paginator.get_page(page_number)
    context = {
        **common_context,
        'page_title': category.name,
        'articles': articles_page,
        'active_category': category_slug,
    }
    return render(request, 'news/index.html', context)

def tag_view(request, tag_slug):
    """Displays articles associated with a specific tag, with pagination."""
    common_context = _get_common_context()
    tag = get_object_or_404(Tag, slug=tag_slug)
    article_list = tag.articles.all().order_by('-published_at')
    paginator = Paginator(article_list, 10)
    page_number = request.GET.get('page')
    articles_page = paginator.get_page(page_number)
    context = {
        **common_context,
        'page_title': f"#{tag.name} tegi bo'yicha yangiliklar",
        'articles': articles_page,
        'active_category': None,
    }
    return render(request, 'news/index.html', context)

def search_view(request):
    """Displays search results, with pagination."""
    common_context = _get_common_context()
    query = request.GET.get('q', '')
    if query:
        article_list = Article.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(content__icontains=query)
        ).order_by('-published_at').distinct()
        page_title = f'Qidiruv natijalari: "{query}"'
    else:
        article_list = Article.objects.none()
        page_title = 'Qidiruv'
    paginator = Paginator(article_list, 10)
    page_number = request.GET.get('page')
    articles_page = paginator.get_page(page_number)
    context = {
        **common_context,
        'page_title': page_title,
        'articles': articles_page,
        'active_category': None,
    }
    return render(request, 'news/index.html', context)

def article_detail_view(request, slug):
    """Displays a single article and handles comment form submission."""
    common_context = _get_common_context()
    article = get_object_or_404(Article, slug=slug)
    if request.method == 'POST':
        author_name = request.POST.get('author')
        comment_body = request.POST.get('body')
        if author_name and comment_body:
            Comment.objects.create(article=article, author=author_name, body=comment_body)
            return redirect('article_detail_view', slug=article.slug)
    context = {
        **common_context,
        'page_title': article.title,
        'article': article,
        'active_category': article.category.slug if article.category else None,
    }
    return render(request, 'news/article_detail.html', context)

@login_required
def add_article_view(request):
    """
    Handles adding a new article.
    """
    common_context = _get_common_context()

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            # ✅ FIXED: Added allow_unicode=True to handle non-ASCII characters
            article.slug = slugify(article.title, allow_unicode=True)
            article.save()
            form.save_m2m() # Save the many-to-many relationships (tags)
            messages.success(request, f"Maqola '{article.title}' muvaffaqiyatli saqlandi.")
            return redirect('article_detail_view', slug=article.slug)
        else:
            messages.error(request, "Maqolani saqlashda xatolik yuz berdi. Iltimos, xatolarni to'g'rilang.")
    else:
        # GET request, show a blank form
        form = ArticleForm()

    context = {
        **common_context,
        'page_title': "Yangi maqola qo'shish",
        'form': form,
    }
    return render(request, 'news/add_article.html', context)
