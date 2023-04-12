from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from app_users.models import Profile


class RegistrationTest(TestCase):
    """ Tests for registration procedure """
    def test_url_exists_at_correct_location(self):
        response = self.client.get('/users/register/')
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/register.html')

    def test_template_content(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text='<title>Регистрация</title>')
        self.assertNotContains(response, "Not on the page")

    def test_post_incorrect_data(self):
        user_data = {'username': 'testUser_4', 'password1': '1X<ISRUkw+tuK'}
        response = self.client.post(reverse('register'), data=user_data)
        self.assertEqual(response.status_code, 200)
        user = get_user_model().objects.filter(pk=1).exists()
        self.assertFalse(user)

    def test_post_correct_data(self):
        user_data = {'username': 'testUser_4', 'password1': '1X<ISRUkw+tuK',
                     'password2': '1X<ISRUkw+tuK'}
        response = self.client.post(reverse('register'), data=user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main'))
        user = get_user_model().objects.get(id=1)
        self.assertEqual(user.username, 'testUser_4')
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.user, user)
