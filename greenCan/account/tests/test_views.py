from django.test import TestCase, Client
from django.urls import reverse
from account.views import *


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()


    def test_login_GET(self):

        response = self.client.get(reverse('account:login'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/templates/login.html')


    def test_signup_GET(self):

        response = self.client.get(reverse('account:create'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/templates/signup.html')

        
    def test_reset_password_GET(self):

        response = self.client.get(reverse('account:reset-password'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/templates/reset-password.html')


    def test_forget_password_GET(self):

        response = self.client.get(reverse('account:forget-password'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/templates/forget-password.html')
