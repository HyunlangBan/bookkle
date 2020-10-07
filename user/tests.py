from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import (
    urlsafe_base64_encode, 
    urlsafe_base64_decode
)

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from user.models import User, Follow
from user.token import account_activation_token 
from my_settings import EMAIL

class SignUpViewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="originaluser@email.com",
            nickname="test",
            password="test-pwd"
        )
        self.user.is_active = True
        self.user.save()

    def test_signup_success(self):
        data = {"email": "test@email.com", "nickname":"hello", "password":"test-pwd"}
        response = self.client.post('/accounts/signup', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_signup_409_error_duplicated_email(self):
        data = {"email": "originaluser@email.com", "nickname":"hello", "password":"test-pwd"}
        response = self.client.post('/accounts/signup', data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertTrue(response.data['email'])

    def test_signup_409_error_duplicated_nickname(self):
        data = {"email": "test@email.com", "nickname":"test", "password":"test-pwd"}
        response = self.client.post('/accounts/signup', data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertTrue(response.data['nickname'])

class LogInViewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email = "test@email.com",
            nickname = "nick",
            password = "test-pwd"
        )
        self.user.is_active = True
        self.user.save()

    def test_signin_success(self):
        data = {"email": "test@email.com", "password":"test-pwd"}
        res = self.client.post('/accounts/signin', data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_signin_incorrect_password(self):
        data = {"email": "test@email.com", "password":"incorrect-pwd"}
        res = self.client.post('/accounts/signin', data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signin_incorrect_email(self):
        data = {"email": "incorrect_email@email.com", "password":"test-pwd"}
        res = self.client.post('/accounts/signin', data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_inactive_user_login_fail(self):
        inactive_user = User.objects.create_user(
            nickname="new_user", 
            email="new@email.com", 
            password="test_pwd"
        )
        data = {"email": "new@email.com", "password": "test_pwd"}
        res = self.client.post('/accounts/signin', data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

class UserProfileViewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email = "test@email.com",
            nickname = "nick",
            password = "test-pwd"
        )
        self.user.is_active = True
        self.user.save()

    def test_everyone_retrieve_user_profile_success(self):
        res = self.client.get(reverse('user-profile', kwargs={'pk': self.user.id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_profile_404_not_found(self):
        res = self.client.get('accounts/profile/100')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

class MyReviewViewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email = "test@email.com",
            nickname = "nick",
            password = "test-pwd"
        )
        self.user.is_active = True
        self.user.save()

    def test_everyone_my_review_list_success(self):
        res = self.client.get(reverse('my-reviews', kwargs={'pk': self.user.id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_review_list_404_not_found(self):
        res = self.client.get('reviews/my-reviews/100')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

class FollowToggleViewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email = "test@email.com",
            nickname = "nick",
            password = "test-pwd"
        )
        self.user.is_active = True
        self.user.save()

        self.follower = User.objects.create_user(
            email = "follower@email.com",
            nickname = "follower",
            password = "test-pwd"
        )
        self.follower.is_active = True
        self.follower.save()

        self.token = Token.objects.create(user=self.follower)
        self.token_authentication()

    def token_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)

    def test_follow_success(self):
        data = {"follow_to": self.user.id}
        res = self.client.post(reverse('follow'), data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_unfollow_success(self):
        data = {"follow_to": self.user.id}
        self.client.post(reverse('follow'), data)
        res = self.client.post(reverse('follow'), data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['message'], 'UNFOLLOW SUCCESS')

    def test_follow_fail_un_authenticated(self):
        self.client.force_authenticate(user=None)
        data = {"follow_to": self.user.id}
        res = self.client.post(reverse('follow'), data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.data['message'], 'NEED_LOGIN')
        
class ActivateTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email = "test@email.com",
            nickname = "nick",
            password = "test-pwd"
        )

        self.user2 = User.objects.create_user(
            email = "test2@email.com",
            nickname = "guest",
            password = "test-pwd"
        )

    def test_activate_user_success(self):
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = account_activation_token.make_token(self.user)
        res = self.client.get(f'/accounts/activate/{uidb64}/{token}')
        self.assertRedirects(res, EMAIL['REDIRECT_PAGE'], status_code=302, target_status_code=200, fetch_redirect_response=True)
        
    def test_activate_user_not_found_error(self):
        uidb64 = urlsafe_base64_encode(force_bytes(1000000))
        token = account_activation_token.make_token(self.user)
        res = self.client.get(f'/accounts/activate/{uidb64}/{token}')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        

    def test_activate_user_token_error(self):
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = account_activation_token.make_token(self.user2)
        res = self.client.get(f'/accounts/activate/{uidb64}/{token}')
        
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.data['message'], 'INVALID_TOKEN')

