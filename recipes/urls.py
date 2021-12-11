from django.urls import path 
from . import views
from .feeds import LatestPostsFeed

# API views
from .views import PostDetail, PostList

app_name = 'recipes'
urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('search/', views.post_search, name='post_search'),
    path('feed/', LatestPostsFeed(), name='post_feed'),

    # for API
    path('', PostList.as_view()),
    path('<int:pk>/', PostDetail.as_view()),
]