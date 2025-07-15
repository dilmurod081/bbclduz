# news/forms.py

from django import forms
from .models import Article, Category, Tag

class ArticleForm(forms.ModelForm):
    # Use ModelChoiceField for a dropdown selector for the category
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'w-full p-2 border rounded-md bg-slate-50 focus:outline-none focus:ring-2 focus:ring-blue-500'})
    )
    # Use ModelMultipleChoiceField for a multi-select box for tags
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'w-full p-2 border rounded-md bg-slate-50 focus:outline-none focus:ring-2 focus:ring-blue-500', 'size': '5'}),
        required=False
    )

    class Meta:
        model = Article
        fields = ['title', 'description', 'content', 'image_url', 'category', 'tags', 'is_lead']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-md bg-slate-50 focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'w-full p-2 border rounded-md bg-slate-50 focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'content': forms.Textarea(attrs={'rows': 10, 'class': 'w-full p-2 border rounded-md bg-slate-50 focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'image_url': forms.URLInput(attrs={'class': 'w-full p-2 border rounded-md bg-slate-50 focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'is_lead': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-blue-600 rounded border-gray-300 focus:ring-blue-500'}),
        }
