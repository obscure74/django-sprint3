from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Category


def index(request):
    """
    Отображает главную страницу
    с пятью последними опубликованными постами.
    """
    # Текущее время для проверки даты публикации
    current_time = timezone.now()

    post_list = Post.objects.filter(
        is_published=True,
        pub_date__lte=current_time,
        category__is_published=True
    ).select_related('category', 'location', 'author') \
     .order_by('-pub_date')[:5]

    return render(request, 'blog/index.html', {'posts': post_list})


def post_detail(request, post_id):
    """Отображает детальную страницу поста по ID."""
    current_time = timezone.now()

    post = get_object_or_404(
        Post.objects.select_related('category', 'location', 'author'),
        id=post_id,
        is_published=True,
        pub_date__lte=current_time,
        category__is_published=True
    )

    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    """Отображает страницу категории."""
    current_time = timezone.now()

    # Получаем категорию, проверяем что она опубликована
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug
    )

    # Получаем посты для этой категории
    post_list = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=current_time
    ).select_related('location', 'author').order_by('-pub_date')

    return render(
        request,
        'blog/category.html',
        {'category': category, 'posts': post_list}
    )
