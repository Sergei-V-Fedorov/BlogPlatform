from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings


class LoginTest(TestCase):
    """ Tests for login procedure """
    def test_url_exists_at_correct_location(self):
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/login.html')

    def test_template_content(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text='<title>Аутенификация</title>')
        self.assertNotContains(response, "Not on the page")

    def test_login_post_incorrect_data(self):
        user_data = {'username': 'test', 'password': 'querty1234'}
        response = self.client.post(reverse('login'), data=user_data)
        self.assertEqual(response.status_code, 200)

    def test_login_post_correct_data(self):
        get_user_model().objects.create_user(username='testUser_4',
                                             password='1X<ISRUkw+tuK',
                                             first_name='Name', last_name='Surname')
        user_data = {'username': 'testUser_4', 'password': '1X<ISRUkw+tuK'}
        response = self.client.post(reverse('login'), data=user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, settings.LOGIN_REDIRECT_URL)
