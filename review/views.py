from django.db.models import Count
from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import (
        SessionAuthentication,
        TokenAuthentication
)
from review.serializers import ReviewListSerializer, ReviewCreateSerializer
from review.models import Review, Recommand, Book
from user.models import User
from rest_framework.response import Response
import datetime


class ReviewViewSet(viewsets.ModelViewSet):
#### TEST 데이터에 맞추기 위해 잠시 커맨트처리
#    DAYS = 30
#    posted_time = datetime.datetime.now() - datetime.timedelta(DAYS)
#    now = datetime.datetime.now()
#    queryset = Review.objects.filter(created_at__range=[posted_time, now]).order_by('-recommand_count')
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Review.objects.order_by('-recommand_count')
    serializer_class = ReviewListSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer_class = ReviewCreateSerializer(data=data)
        serializer_class.is_valid()
        book = Book.objects.get_or_create(title=data['book_title'], author=data['book_author'], image=data['book_image'])[0]
        Review.objects.create(book=book, title = data['title'], content = data['content'], rating = data['rating'], quote = data['quote'], user=request.user)
        return Response(serializer_class.data)
