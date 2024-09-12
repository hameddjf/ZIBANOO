from django.views.generic import ListView, DetailView
from .models import Category, Tag


class CategoryListView(ListView):
    """List view for categories"""
    model = Category
    context_object_name = 'categories'
    # template_name = 'categories/category_list.html'


class CategoryDetailView(DetailView):
    """Detail view for a category"""
    model = Category
    context_object_name = 'category'
    # template_name = 'categories/category_detail.html'


class TagListView(ListView):
    """List view for tags"""
    model = Tag
    context_object_name = 'tags'
    # template_name = 'categories/tag_list.html'


class TagDetailView(DetailView):
    """Detail view for a tag"""
    model = Tag
    context_object_name = 'tag'
    # template_name = 'categories/tag_detail.html'
