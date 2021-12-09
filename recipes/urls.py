from django.urls import path 
from . import views

# API views
# from .views import PostDetail, PostList

app_name = 'recipes'
urlpatterns = [
    # post views
    # path('', views.post_list, name='post_list'),
    # path('', views.PostListView.as_view(), name='post_list'),
    path('', views.post_list, name='post_list'),
    # path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    # path('<int:post_id>/share/', views.post_share, name='post_share'),

    # for API
    # path('api_v1/<int:pk>/', PostDetail.as_view()),
    # path('api_v1/', PostList.as_view()),
]