from rest_framework import viewsets, status, generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import get_user_model

from user.serializers import UserSerializer, LoginSerializer, UserProfileSerializer
from user.models import User
from user.token import account_activation_token 
from user.text import message
from my_settings import EMAIL, DOMAIN
from review.models import Review
from review.serializers import ReviewListSerializer


class SignUpView(generics.CreateAPIView):
    def create(self, request):
        data = request.data
        serializer_class = UserSerializer(data=data) 
        if serializer_class.is_valid(): 
            user = User.objects.create_user(data['email'], data['nickname'], data['password'])
            current_site = get_current_site(request)
            #domain = current_site.domain
            domain = DOMAIN
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            message_data = message(domain, uidb64, token)
     
            mail_title = "[Bookkle] 이메일 인증을 완료해주세요"
            mail_to = data['email']
            email = EmailMessage(mail_title, message_data, to=[mail_to])
            email.send()
            return Response({"message":"SUCCESS"})
        return Response(serializer_class.errors, status=status.HTTP_409_CONFLICT)


class Activate(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                return redirect(EMAIL['REDIRECT_PAGE'])
            return Response({"message":"SUCCESS"})
        except ValidationError:
            return Response({"message": "TYPE_ERROR"})
        except KeyError:
            return Response({"message": "INVALID_KEY"})

class LoginView(APIView):
    def post(self, request):
        data = request.data
        email = data['email']
        password = data['password']
        serializer_class = LoginSerializer(data = data)
        if serializer_class.is_valid(raise_exception = True):
            user = serializer_class.validated_data
            token = Token.objects.get_or_create(user=user)
            return Response({"token": str(token[0])})
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

class MyReviewView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReviewListSerializer

    def get_queryset(self):
        queryset = Review.objects.filter(user = self.request.user)
        return queryset


class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    def retrieve(self, request):
        user = User.objects.get(id = request.user.id)
        serializer_class = UserProfileSerializer(user)
        return Response(serializer_class.data)
