from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from review.models import (
    Book,
    Review,
    Recommend
)
from user.models import (
    User,
    Follow
)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname']

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
        exclude = ['recommend_count', 'user', 'book', 'recommender']

class ReviewListSerializer(serializers.ModelSerializer):
    book_detail = BookSerializer(source='book')
    user_info = UserProfileSerializer(source='user', read_only = True)

    class Meta:
        model = Review
        fields = ['id', 'title', 'content', 'rating','quote', 'recommend_count', 'book_detail', 'user_info']
        read_only_fields = ['recommend_count']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ['recommend_count', 'created_at', 'updated_at', 'book', 'user']

        def update(self, instance, validated_data):
            instance.title = validated_data.get('title', instance.title)
            instance.content = validated_data.get('content', instance.content)
            instance.quote = validated_data.get('quote', instance.quote)
            instance.rating = validated_data.get('rating', instance.rating)
            return instance

class RecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommend
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Recommend.objects.all(),
                fields=['review', 'user'],
                message = "Duplicated Recommend"
            )
        ]
