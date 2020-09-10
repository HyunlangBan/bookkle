from django.db.models import Count
from rest_framework import viewsets, status
from review.serializers import ReviewListSerializer, ReviewCreateSerializer
from review.models import Review, Recommand, Book
from user.models import User
from rest_framework.response import Response
import datetime

class ReviewViewSet(viewsets.ModelViewSet):
#### TEST 데이터에 맞추기 위해 잠시 커맨트처리ㅓ
#    DAYS = 30
#    posted_time = datetime.datetime.now() - datetime.timedelta(DAYS)
#    now = datetime.datetime.now()
#    queryset = Review.objects.filter(created_at__range=[posted_time, now]).order_by('-recommand_count')

    queryset = Review.objects.order_by('-recommand_count')
    serializer_class = ReviewListSerializer

    def create(self, request, *args, **kwargs):
        serializer_class = ReviewCreateSerializer
        ######## user 추가 필요
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
