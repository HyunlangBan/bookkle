from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from review.models import (
    Book,
    Review,
    Like
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
        exclude = ['like_count', 'user', 'book', 'liker']

class ReviewListSerializer(serializers.ModelSerializer):
    book_detail = BookSerializer(source='book')
    user_info = UserProfileSerializer(source='user', read_only = True)

    class Meta:
        model = Review
        fields = ['id', 'title', 'content', 'rating','quote', 'like_count', 'book_detail', 'user_info']
        read_only_fields = ['like_count']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ['like_count', 'created_at', 'updated_at', 'book', 'user']

        def update(self, instance, validated_data):
            instance.title = validated_data.get('title', instance.title)
            instance.content = validated_data.get('content', instance.content)
            instance.quote = validated_data.get('quote', instance.quote)
            instance.rating = validated_data.get('rating', instance.rating)
            return instance

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Like.objects.all(),
                fields=['review', 'user'],
                message = "Duplicated Like"
            )
        ]
