# news/views.py

from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Article, Category, Tag # Assuming you have an Opinion model as well

# --- Helper Function for Common Context ---
def _get_common_context():
    """
    Returns a dictionary with context data needed on almost every page.
    This avoids repeating code in every view (DRY principle).
    """
    return {
        'categories': Category.objects.all(),
        'popular_tags': Tag.objects.all()[:10],
        'recent_comments': Comment.objects.order_by('-created_at')[:4],# Example: get 10 most popular tags
    }

# --- Main Views ---
def home(request):
    """
    Displays the home page with a paginated list of all articles.
    """
    common_context = _get_common_context()
    article_list = Article.objects.all().order_by('-published_at')

    # Setup pagination
    paginator = Paginator(article_list, 10) # Show 10 articles per page (1 lead + 9 grid)
    page_number = request.GET.get('page')
    articles_page = paginator.get_page(page_number)

    context = {
        **common_context, # Unpack the common context dictionary
        'page_title': 'Bosh sahifa',
        'articles': articles_page,
        'active_category': None, # No category is active on the home page
        'latest_news': article_list[:5], # Use the already fetched list for efficiency
    }
    return render(request, 'news/index.html', context)


def category_view(request, category_slug):
    """
    Displays articles for a specific category, with pagination.
    """
    common_context = _get_common_context()
    category = get_object_or_404(Category, slug=category_slug)
    article_list = Article.objects.filter(category=category).order_by('-published_at')

    # Setup pagination
    paginator = Paginator(article_list, 10) # Show 10 articles per page
    page_number = request.GET.get('page')
    articles_page = paginator.get_page(page_number)

    context = {
        **common_context,
        'page_title': category.name,
        'articles': articles_page,
        'active_category': category_slug, # To set the active class in nav
        'latest_news': Article.objects.order_by('-published_at')[:5],
    }
    return render(request, 'news/index.html', context)


def tag_view(request, tag_slug):
    """
    Displays articles associated with a specific tag, with pagination.
    """
    common_context = _get_common_context()
    tag = get_object_or_404(Tag, slug=tag_slug)
    article_list = tag.articles.all().order_by('-published_at')

    # Setup pagination
    paginator = Paginator(article_list, 10)
    page_number = request.GET.get('page')
    articles_page = paginator.get_page(page_number)

    context = {
        **common_context,
        'page_title': f"#{tag.name} tegi bo'yicha yangiliklar",
        'articles': articles_page,
        'active_category': None, # No category is active on tag view
        'latest_news': Article.objects.order_by('-published_at')[:5],
    }
    return render(request, 'news/index.html', context)


def search_view(request):
    """
    Displays search results, with pagination.
    """
    common_context = _get_common_context()
    query = request.GET.get('q', '')

    if query:
        article_list = Article.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).order_by('-published_at')
        page_title = f'Qidiruv natijalari: "{query}"'
    else:
        article_list = Article.objects.none() # Return no articles if query is empty
        page_title = 'Qidiruv'

    # Setup pagination
    paginator = Paginator(article_list, 10)
    page_number = request.GET.get('page')
    articles_page = paginator.get_page(page_number)

    context = {
        **common_context,
        'page_title': page_title,
        'articles': articles_page, # Use 'articles' to match the template
        'active_category': None,
        'latest_news': Article.objects.order_by('-published_at')[:5],
    }
    return render(request, 'news/index.html', context)

from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect # Make sure to import redirect
from django.core.paginator import Paginator
from .models import Article, Category, Tag, Opinion, Comment

def article_detail_view(request, slug):
    """
    Displays a single article and handles comment form submission.
    """
    common_context = _get_common_context()
    article = get_object_or_404(Article, slug=slug)

    # --- ✅ ADD THIS LOGIC ---
    # Handle comment form submission (POST request)
    if request.method == 'POST':
        author_name = request.POST.get('author')
        comment_body = request.POST.get('body')

        if author_name and comment_body:
            # Create a new comment object and link it to the article
            Comment.objects.create(
                article=article,
                author=author_name,
                body=comment_body
            )
            # Redirect back to the same article page to see the new comment
            # and prevent form resubmission on refresh.
            return redirect('article_detail_view', slug=article.slug)
    # --- END OF NEW LOGIC ---

    # This part handles the initial page load (GET request)
    context = {
        **common_context,
        'page_title': article.title,
        'article': article,
        'active_category': article.category.slug if article.category else None,
    }
    return render(request, 'news/article_detail.html', context)