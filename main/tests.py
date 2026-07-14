from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import BlogPost


class BlogAccessTests(TestCase):
    def setUp(self):
        self.post = BlogPost.objects.create(
            title='Test post',
            content='Test content',
        )
        self.staff_user = get_user_model().objects.create_user(
            username='staff',
            password='test-password',
            is_staff=True,
        )

    def test_blog_reading_is_public(self):
        self.assertEqual(self.client.get(reverse('blog_list')).status_code, 200)
        self.assertEqual(
            self.client.get(reverse('blog_detail', args=[self.post.pk])).status_code,
            200,
        )

    def test_blog_management_redirects_anonymous_users(self):
        protected_urls = [
            reverse('blog_create'),
            reverse('blog_update', args=[self.post.pk]),
            reverse('blog_delete', args=[self.post.pk]),
        ]

        for url in protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(
                    response,
                    f"{reverse('admin:login')}?next={url}",
                )

    def test_staff_users_can_open_blog_management_pages(self):
        self.client.force_login(self.staff_user)

        self.assertEqual(self.client.get(reverse('blog_create')).status_code, 200)
        self.assertEqual(
            self.client.get(reverse('blog_update', args=[self.post.pk])).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(reverse('blog_delete', args=[self.post.pk])).status_code,
            200,
        )
