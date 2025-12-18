from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import STR_MAX_LENGTH

User = get_user_model()


class PublishedModel(models.Model):
    """Абстрактная модель с общими полями is_published и created_at."""

    is_published = models.BooleanField(
        default=True,
        verbose_name=_('Опубликовано'),
        help_text=_('Снимите галочку, чтобы скрыть публикацию.')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Добавлено')
    )

    class Meta:
        abstract = True


class Category(PublishedModel):
    """Тематическая категория."""

    title = models.CharField(
        max_length=256,
        verbose_name=_('Заголовок')
    )
    description = models.TextField(
        verbose_name=_('Описание')
    )
    slug = models.SlugField(
        unique=True,
        verbose_name=_('Идентификатор'),
        help_text=_(
            'Идентификатор страницы для URL; разрешены символы '
            'латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = _('категория')
        verbose_name_plural = _('Категории')

    def __str__(self):
        title_part = self.title[:STR_MAX_LENGTH]
        if len(self.title) > STR_MAX_LENGTH:
            return f'{title_part}...'
        return title_part


class Location(PublishedModel):
    """Географическая метка."""

    name = models.CharField(
        max_length=256,
        verbose_name=_('Название места')
    )

    class Meta:
        verbose_name = _('местоположение')
        verbose_name_plural = _('Местоположения')

    def __str__(self):
        name_part = self.name[:STR_MAX_LENGTH]
        if len(self.name) > STR_MAX_LENGTH:
            return f'{name_part}...'
        return name_part


class Post(PublishedModel):
    """Публикация."""

    title = models.CharField(
        max_length=256,
        verbose_name=_('Заголовок')
    )
    text = models.TextField(
        verbose_name=_('Текст')
    )
    pub_date = models.DateTimeField(
        verbose_name=_('Дата и время публикации'),
        help_text=_(
            'Если установить дату и время в будущем — можно делать '
            'отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Автор публикации'),
        related_name='posts'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Местоположение'),
        related_name='posts'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Категория'),
        related_name='posts'
    )

    class Meta:
        verbose_name = _('публикация')
        verbose_name_plural = _('Публикации')
        ordering = ['-pub_date']
        default_related_name = 'posts'

    def __str__(self):
        title_part = self.title[:STR_MAX_LENGTH]
        if len(self.title) > STR_MAX_LENGTH:
            return f'{title_part}...'
        return title_part
