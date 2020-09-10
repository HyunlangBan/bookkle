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
    class Meta:
        model = Review
        exclude = ['recommand_count']

class ReviewListSerializer(serializers.ModelSerializer):
    book_detail = BookSerializer(source='book', read_only = True)
    user_info = UserProfileSerializer(source='user', read_only = True)

    class Meta:
        model = Review
        fields = ['id','title', 'book', 'user', 'content', 'rating','quote', 'recommand_count', 'book_detail', 'user_info']
        read_only_fields = ['recommand_count']



