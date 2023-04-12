from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from app_users.models import Profile
from django.core.files.uploadedfile import SimpleUploadedFile
import os


class ProfileViewTest(TestCase):
    """ Tests for profile view functionality """
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='testUser_4',
                                                        password='1X<ISRUkw+tuK')
        Profile.objects.create(user=cls.user)

    def setUp(self):
        self.client.login(username='testUser_4', password='1X<ISRUkw+tuK')

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login/?next=/users/profile/')

    def test_url_exists_at_correct_location(self):
        response = self.client.get('/users/profile/')
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/profile.html')

    def test_template_content(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text='Профиль пользователя')
        self.assertEqual(str(response.context['user']), self.user.username)
        self.assertNotContains(response, "Not on the page")


class ProfileEditTest(TestCase):
    """ Tests for profile edit functionality """
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='testUser_4',
                                                        password='1X<ISRUkw+tuK',
                                                        first_name='Name', last_name='Surname')
        cls.profile = Profile.objects.create(user=cls.user)
        cls.pk = cls.profile.id
        cls.url = f'/users/profile/{cls.pk}/edit/'
        cls.url_name = reverse('profile-edit', args=[cls.pk])

    def setUp(self):
        self.client.login(username='testUser_4', password='1X<ISRUkw+tuK')

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url_name)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/users/login/?next={self.url}')

    def test_url_exists_at_correct_location(self):
        response = self.client.get(self.url_name)
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(self.url_name)
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(self.url_name)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/profile-edit.html')

    def test_template_content(self):
        response = self.client.get(self.url_name)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text='Редактирование профиля пользователя')
        self.assertTrue(response.context['form'])
        self.assertEqual(response.context['form'].initial['first_name'],
                         self.user.first_name)
        self.assertEqual(response.context['form'].initial['last_name'],
                         self.user.last_name)
        self.assertEqual(response.context['form'].instance, self.profile)
        self.assertNotContains(response, "Not on the page")

    def test_post_correct_data_without_avatar(self):
        user_data = {'first_name': 'new_name',
                     'last_name': 'new_surname'}
        response = self.client.post(self.url_name, data=user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'))
        profile = Profile.objects.first()
        self.assertEqual(profile.user.first_name, 'new_name')
        self.assertEqual(profile.user.last_name, 'new_surname')

    def test_post_correct_data_with_avatar(self):
        file_dir = './app_blogs/tests/'
        file_name = 'django-icon_1.png'
        file = open(os.path.join(file_dir, file_name), 'rb')
        file_data = SimpleUploadedFile(file_name, file.read())
        user_data = {'first_name': 'new_name',
                     'last_name': 'new_surname',
                     'avatar': file_data}
        response = self.client.post(self.url_name, data=user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'))
        profile = Profile.objects.first()
        self.assertEqual(profile.user.first_name, 'new_name')
        self.assertEqual(profile.user.last_name, 'new_surname')
        self.assertTrue(str(profile.avatar).find(file_name[:-4]))
