from rest_framework import serializers
from rest_framework.response import Response

from django.contrib.auth import authenticate

from user.models import User

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

    def field_check(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Duplicated Email")
        elif User.objects.filter(nickname=data['nickname']).exists():
            raise serializers.ValidationError("Duplicated Nickname")
        return True
