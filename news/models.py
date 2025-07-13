# news/models.py

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    # ... (rest of the model is fine)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    # ... (rest of the model is fine)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    image_url = models.URLField(max_length=500, help_text="Rasmga to'g'ridan-to'g'ri URL manzil")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles')
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles')
    published_at = models.DateTimeField(auto_now_add=True)

    # ✅ FIXED: Added the missing 'is_lead' field.
    is_lead = models.BooleanField(default=False,
                                  help_text="Belgilansa, bu yangilik bosh sahifada asosiy bo'lib ko'rinadi")

    def get_absolute_url(self):
        return reverse('article_detail_view', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.article}'


# ✅ FIXED: Added the missing 'Opinion' model.
class Opinion(models.Model):
    quote = models.TextField(help_text="Fikr-mulohaza matni")
    author = models.CharField(max_length=150, help_text="Fikr-mulohaza muallifi")

    class Meta:
        verbose_name = "Fikr-mulohaza"
        verbose_name_plural = "Fikr-mulohazalar"

    def __str__(self):
        return f'"{self.quote[:50]}..." - {self.author}'