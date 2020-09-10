from rest_framework import serializers
from rest_framework.response import Response

from user.models import (
    User
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


    def field_check(self, data):
        print("validation start")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Duplicated Email")
        elif User.objects.filter(nickname=data['nickname']).exists():
            raise serializers.ValidationError("Duplicated Nickname")
        return True
