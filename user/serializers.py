from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.validators import UniqueTogetherValidator

from django.contrib.auth import authenticate

from user.models import User, Follow

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
   
    def validate(self, data):
        user = authenticate(**data)
        if user is None:
            raise serializers.ValidationError("INVALID USER")
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__' 

class UserProfileSerializer(serializers.ModelSerializer):
    is_follow = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'follower_count', 'nickname', 'is_follow']

    def get_is_follow(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            follow_list = user.following.all()
            if obj in follow_list:
                return True
            return False
        return False

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['follow_from', 'follow_to'],
                message = "Duplicated Follow"
            )
        ]
