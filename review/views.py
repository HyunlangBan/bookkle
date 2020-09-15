import datetime
import random

from django.db.models import Count

from rest_framework import (
    viewsets, 
    status, 
    permissions, 
    generics
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from review.serializers import ( 
    ReviewSerializer,
    ReviewListSerializer, 
    ReviewCreateSerializer,
    LikeSerializer
)
from review.models import (
    Review, 
    Like, 
    Book
)
from user.models import User
from user.permissions import IsReviewAuthorOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
#### django-seed TEST 데이터에 맞추기 위해 잠시 커맨트처리
#    DAYS = 30
#    posted_time = datetime.datetime.now() - datetime.timedelta(DAYS)
#    now = datetime.datetime.now()
#    queryset = Review.objects.filter(created_at__range=[posted_time, now]).order_by('-like_count')
    queryset = Review.objects.order_by('-like_count')
    serializer_class = ReviewListSerializer
    #permission_classes = [IsReviewAuthorOrReadOnly]
    
    def create(self, request):
        data = request.data
        serializer_class = ReviewCreateSerializer(data=data)
        if serializer_class.is_valid():
            book = Book.objects.get_or_create(title=data['book_title'], author=data['book_author'], image=data['book_image'])[0]
            review = Review.objects.create(book=book, title = data['title'], content = data['content'], rating = data['rating'], quote = data['quote'], user=request.user)
            return Response({"message": "SUCCESS"})
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, **kwargs):
        data = request.data
        review = Review.objects.get(id = kwargs['pk'])
        serializer_class = ReviewSerializer(review, data = data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data)


class RandomQuoteView(APIView):
    def get(self, request):
        queryset = Review.objects.filter(quote__isnull = False)
        try:
            today_book = random.choice(queryset)
            quote = today_book.quote
            title = today_book.book.title
            author = today_book.book.author
            return Response({"quote": quote, "book_title":title, "book_author": author})
        except IndexError:
            return Response({"quote": "Welcome to Bookkle!"})
    

class LikeView(generics.CreateAPIView):
   permission_classes = [IsAuthenticated]

   def create(self, request):
       data = request.data.copy()
       data['user'] = request.user.id
       serializer_class = LikeSerializer(data = data)
       review = Review.objects.get(id = data['review'])
       if serializer_class.is_valid():
           serializer_class.save()
           review.like_count += 1
           review.save()
           return Response({"like_count": review.like_count})
       Like.objects.get(user=request.user, review=review).delete()
       review.like_count -= 1
       review.save()
       return Response({"undo_like_count": review.like_count})
