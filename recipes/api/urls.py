from django.urls import path 

# API views
from .views import UserList, UserDetail, PostDetail, PostList


urlpatterns = [
    # for API
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('', PostList.as_view()),
    path('<int:pk>/', PostDetail.as_view()),
]



