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
