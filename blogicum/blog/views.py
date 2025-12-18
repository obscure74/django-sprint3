from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .constants import POST_TEXT_TRUNCATE_WORDS, POSTS_ON_INDEX_PAGE
from .models import Category, Post


def get_published_posts():
    """
    Возвращает базовый QuerySet опубликованных постов.

    Включает фильтрацию по:
    - is_published=True
    - pub_date не позже текущего времени
    - category__is_published=True
    """
    current_time = timezone.now()
    return Post.objects.filter(
        is_published=True,
        pub_date__lte=current_time,
        category__is_published=True
    ).select_related('category', 'location', 'author')


def index(request):
    """
    Отображает главную страницу.

    Показывает пять последних опубликованных постов.

    Returns:
        HttpResponse: Отрендеренный шаблон blog/index.html
    """
    posts = get_published_posts()[:POSTS_ON_INDEX_PAGE]

    return render(request, 'blog/index.html', {
        'posts': posts,
        'truncate_words': POST_TEXT_TRUNCATE_WORDS
    })


def post_detail(request, post_id):
    """
    Отображает детальную страницу поста по ID.

    Args:
        post_id: ID поста для отображения

    Returns:
        HttpResponse: Отрендеренный шаблон blog/detail.html

    Raises:
        Http404: если пост не найден или не опубликован
    """
    post = get_object_or_404(
        get_published_posts(),
        id=post_id
    )

    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    """
    Отображает страницу категории с постами.

    Args:
        category_slug: slug категории для отображения

    Returns:
        HttpResponse: Отрендеренный шаблон blog/category.html

    Raises:
        Http404: если категория не найдена или не опубликована
    """
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug
    )

    posts = get_published_posts().filter(category=category)

    return render(request, 'blog/category.html', {
        'category': category,
        'posts': posts,
        'truncate_words': POST_TEXT_TRUNCATE_WORDS
    })
