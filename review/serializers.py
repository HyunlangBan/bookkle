from rest_framework import serializers

from review.models import (
    Book,
    Review,
    Recommand
)
from user.models import (
    User,
    Following
)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class ReviewCreateSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField() 
    book_author = serializers.CharField()
    book_image = serializers.URLField()

    class Meta:
        model = Review
        exclude = ['recommand_count', 'user', 'book', 'recommander']

class ReviewListSerializer(serializers.ModelSerializer):
    book_detail = BookSerializer(source='book')
    user_info = UserProfileSerializer(source='user', read_only = True)

    class Meta:
        model = Review
        fields = ['id', 'title', 'content', 'rating','quote', 'recommand_count', 'book_detail', 'user_info']
        read_only_fields = ['recommand_count']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ['recommand_count', 'created_at', 'updated_at', 'book', 'user']

        def update(self, instance, validated_data):
            instance.title = validated_data.get('title', instance.title)
            instance.content = validated_data.get('content', instance.content)
            instance.quote = validated_data.get('quote', instance.quote)
            instance.rating = validated_data.get('rating', instance.rating)
            return instance
