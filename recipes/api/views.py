from django.contrib.auth import get_user_model
from rest_framework import generics
from ..models import Post
from ..permissions import IsAuthorOrReadOnly, IsAdminOrUserOrReadOnly
from ..serializers import PostSerializer, UserSerializer

User = get_user_model()

# Create your views here.
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class UserList(generics.ListCreateAPIView): 
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminOrUserOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

