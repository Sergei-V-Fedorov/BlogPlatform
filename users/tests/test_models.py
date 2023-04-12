from django.test import TestCase
from app_users.models import Profile
from django.contrib.auth import get_user_model


class ProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create_user(username='testUser_1',
                                                    password='1234_qwerty')
        cls.profile = Profile.objects.create(user=user)

    def test_registration_date_label(self):
        field_label = self.profile._meta.get_field('registration_date').verbose_name
        self.assertEqual(field_label, 'registration date')

    def test_avatar_label(self):
        field_label = self.profile._meta.get_field('avatar').verbose_name
        self.assertEqual(field_label, 'avatar')

    def test_str_method(self):
        expected = f'Profile of {self.profile.user}'
        self.assertEqual(str(self.profile), expected)
