from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from user.models import User, Follow
from review.models import Review, Book

class ReviewViewSetTestCase(APITestCase):
    list_url = reverse('review-list')

    data = {
            "title": "test_title",
            "content": "test_content",
            "rating": 1,
            "quote": "",
            "book_title": "book_title",
            "book_author": "book_author",
            "book_image": "http://www.google.com/"
        } 

    def setUp(self):
        self.user = User.objects.create_user(
            email = "test@email.com",
            nickname = "nick",
            password = "test-pwd"
        )
        self.user.is_active = True
        self.user.save()

        self.user2 = User.objects.create_user(
            email = "test2@email.com",
            nickname = "nick2",
            password = "test-pwd"
        )
        self.user2.is_active = True
        self.user2.save()

        self.token = Token.objects.create(user=self.user)
        self.token_authentication()

        self.book = Book.objects.create(
            title = "book_title",
            author = "book_author",
            image = "https://www.google.com/"
        )
        
        self.review = Review.objects.create(
            title = "test_title",
            content = "test_content", 
            rating = 1,
            book = self.book,
            user = self.user
        )

        
    def token_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)

    def test_everyone_review_list(self):
        self.client.force_authenticate(user=None)
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_review_authenticated(self):
        res = self.client.post(self.list_url, self.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_review_key_error(self):
        invalid_data = {
            "title": "test_title",
        } 
        res = self.client.post(self.list_url, invalid_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_review_un_authenticated(self):
        self.client.force_authenticate(user=None)
        res = self.client.post(self.list_url, self.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_retrieve_reveiw_everyone(self):
        self.client.force_authenticate(user=None)
        res = self.client.get(reverse('review-detail', kwargs={"pk": self.review.id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_404_not_found(self):
        res = self.client.get('reviews/100')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_review_only_author_success(self):
        self.data['title'] = "updated_title"
        res = self.client.put(reverse('review-detail', kwargs={"pk": self.review.id}), self.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_404_not_found(self):
        self.data['title'] = "updated_title"
        res = self.client.put('reviews/100', self.data)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_key_error(self):
        invalid_data = {"name": "new_title"}
        res = self.client.put(reverse('review-detail', kwargs={"pk": self.review.id}), invalid_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_fail_un_authenticated(self):
        self.client.force_authenticate(user=None)
        self.data['title'] = "updated_title"
        res = self.client.put(reverse('review-detail', kwargs={"pk": self.review.id}), self.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_fail_not_writer(self):
        user2 = User.objects.get(email='test2@email.com')
        self.client.force_authenticate(user=user2)
        self.data['title'] = "updated_title"
        res = self.client.put(reverse('review-detail', kwargs={"pk": self.review.id}), self.data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_delete_only_author_success(self):
        res = self.client.delete(reverse('review-detail', kwargs={"pk": self.review.id}))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_delete_404_not_found(self):
        res = self.client.delete('reviews/100')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_un_authenticated_fail(self):
        self.client.force_authenticate(user=None)
        res = self.client.delete(reverse('review-detail', kwargs={"pk": self.review.id}))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
 
    def test_delete_not_author_fail(self):
        user2 = User.objects.get(email='test2@email.com')
        self.client.force_authenticate(user=user2)
        res = self.client.delete(reverse('review-detail', kwargs={"pk": self.review.id}))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        
class RandomQuoteTestCase(APITestCase):

    def test_random_quote_success(self):
        Book.objects.create(
            title = "book_title",
            author = "book_author",
            image = "https://www.google.com/"
        )
        res = self.client.get(reverse('random-quote'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_random_quote_is_none(self):
        res = self.client.get(reverse('random-quote'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['quote'], 'Welcome to Bookkle!')
       
class RecommendToggleViewTestCase(APITestCase):

    def setUp(self):
        self.author = User.objects.create_user(
            email = "test@email.com",
            nickname = "nick",
            password = "test-pwd"
        )
        self.author.is_active = True
        self.author.save()

        self.user = User.objects.create_user(
            email = "test2@email.com",
            nickname = "nick2",
            password = "test-pwd"
        )
        self.user.is_active = True
        self.user.save()

        self.token = Token.objects.create(user=self.user)
        self.token_authentication()

        self.book = Book.objects.create(
            title = "book_title",
            author = "book_author",
            image = "https://www.google.com/"
        )
        
        self.review = Review.objects.create(
            title = "test_title",
            content = "test_content", 
            rating = 1,
            book = self.book,
            user = self.author
        )

    def token_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)

    def test_recommend_toggle_authenticated_success(self):
        data = {"review" : self.review.id }
        res = self.client.post(reverse('like'), data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_unlike_authenticated_success(self):
        data = {"review" : self.review.id }
        self.client.post(reverse('like'), data)
        res = self.client.post(reverse('like'), data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['message'], 'LIKE_CANCELLED')

    def test_recommend_toggle_un_authenticated_fail(self):
        self.client.force_authenticate(user=None)
        data = {"review" : self.review.id }
        res = self.client.post(reverse('like'), data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class FollowingReviewViewTestCase(APITestCase):

    def setUp(self):
        self.author = User.objects.create_user(
            email = "test@email.com",
            nickname = "nick",
            password = "test-pwd"
        )
        self.author.is_active = True
        self.author.save()

        self.user= User.objects.create_user(
            email = "test2@email.com",
            nickname = "nick2",
            password = "test-pwd"
        )
        self.user.is_active = True
        self.user.save()

        self.token = Token.objects.create(user=self.user)
        self.token_authentication()

        self.book = Book.objects.create(
            title = "book_title",
            author = "book_author",
            image = "https://www.google.com/"
        )
        
        self.review = Review.objects.create(
            title = "test_title",
            content = "test_content", 
            rating = 1,
            book = self.book,
            user = self.author
        )

        Follow.objects.create(follow_from = self.user, follow_to = self.author)

    def token_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)

    def test_following_review_list_authenticated_success(self):
        res = self.client.get(reverse('following'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_following_review_list_un_authenticated_success(self):
        self.client.force_authenticate(user=None)
        res = self.client.get(reverse('following'))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
