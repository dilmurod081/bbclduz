# news/models.py

from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        verbose_name = "Teg"
        verbose_name_plural = "Teglar"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(verbose_name="Qisqacha mazmuni")
    
    # ✅ FIXED: Added the missing 'content' field for the article's full text.
    content = models.TextField(verbose_name="To'liq matni", default="Maqola matni...")

    image_url = models.URLField(max_length=500, help_text="Rasmga to'g'ridan-to'g'ri URL manzil")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles', verbose_name="Kategoriya")
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles', verbose_name="Teglar")
    published_at = models.DateTimeField(auto_now_add=True, verbose_name="Nashr qilingan sana")
    is_lead = models.BooleanField(default=False, help_text="Belgilansa, bu yangilik bosh sahifada asosiy bo'lib ko'rinadi")

    class Meta:
        verbose_name = "Maqola"
        verbose_name_plural = "Maqolalar"
        ordering = ['-published_at']

    def get_absolute_url(self):
        return reverse('article_detail_view', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            # allow_unicode=True is important for non-latin characters
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name="Maqola")
    author = models.CharField(max_length=100, verbose_name="Muallif")
    body = models.TextField(verbose_name="Sharh matni")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")

    class Meta:
        verbose_name = "Sharh"
        verbose_name_plural = "Sharhlar"
        ordering = ['-created_at']

    def __str__(self):
        return f'Sharh: {self.author} -> {self.article.title}'

class Opinion(models.Model):
    quote = models.TextField(help_text="Fikr-mulohaza matni")
    author = models.CharField(max_length=150, help_text="Fikr-mulohaza muallifi")

    class Meta:
        verbose_name = "Fikr-mulohaza"
        verbose_name_plural = "Fikr-mulohazalar"

    def __str__(self):
        return f'"{self.quote[:50]}..." - {self.author}'
