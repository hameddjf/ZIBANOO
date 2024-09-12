from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<slug:slug>/',
         views.CategoryDetailView.as_view(), name='category_detail'),
    path('tags/', views.TagListView.as_view(), name='tag_list'),
    path('tag/<slug:slug>/', views.TagDetailView.as_view(), name='tag_detail'),
]
