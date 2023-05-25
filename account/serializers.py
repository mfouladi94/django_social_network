from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'email', 'friends_count', 'posts_count', 'get_avatar',)


class FriendshipRequestSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_for = UserSerializer(read_only=True)
    class Meta:
        model = FriendshipRequest
        fields = ('id', 'created_by', 'created_for')