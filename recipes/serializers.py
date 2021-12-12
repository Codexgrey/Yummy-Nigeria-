from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'body', 'created',)


class UserSerializer(serializers.ModelSerializer): # new
    class Meta:
        model = User
        fields = ('id', 'username',)