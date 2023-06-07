from django.test import TestCase
from hotels_app import models
from django.test.client import Client
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse


def create_view_tests(url, page_name, template):
    class ViewTests(TestCase):

        def setUp(self):
            self.client = Client()
            default = 'username'
            self.user = User.objects.create_user(username=default, password=default)
            self.user_client = models.Client.objects.create(user=self.user, phone='79143249943')
            self.client.login(username=default, password=default)

        def test_view_exists_at_url(self):
            self.assertEqual(self.client.get(url).status_code, status.HTTP_200_OK)

        def test_view_exists_by_name(self):
            self.assertEqual(self.client.get(reverse(page_name)).status_code, status.HTTP_200_OK)

        def test_view_uses_template(self):
            resp = self.client.get(reverse(page_name))
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            self.assertTemplateUsed(resp, template)

    return ViewTests


MainPageViewTest = create_view_tests('', 'main page', 'index.html')
FailPageViewTest = create_view_tests('/fail/', 'fail', 'fail.html')
SuccessPageViewTest = create_view_tests('/success/', 'success', 'success.html')
CurrentBookingViewTest = create_view_tests('/bookings/current/', 'current bookings', 'client_bookings.html')
PastBookignViewTest = create_view_tests('/bookings/past/', 'past bookings', 'client_bookings.html')
AccountPageViewTest = create_view_tests('/account/', 'account page', 'account_page.html')
RegisterPageViewTest = create_view_tests('/register/', 'register', 'register.html')
LoginPageViewTest = create_view_tests('/log_in/', 'log in', 'login.html')
