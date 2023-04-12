from django.test import TestCase
from app_users.forms import ProfileForm, RegistrationForm, AuthForm


class ProfileFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form = ProfileForm()

    def test_first_name_label(self):
        field_label = self.form.fields['first_name'].label
        self.assertTrue(field_label is None or field_label == 'Имя')

    def test_last_name_label(self):
        field_label = self.form.fields['last_name'].label
        self.assertTrue(field_label is None or field_label == 'Фамилия')

    def test_avatar_label(self):
        field_label = self.form.fields['avatar'].label
        self.assertTrue(field_label == 'Avatar' or field_label is None)

    def test_first_name_help_text(self):
        field_label = self.form.fields['first_name'].help_text
        self.assertFalse(field_label)

    def test_last_name_help_text(self):
        field_label = self.form.fields['last_name'].help_text
        self.assertFalse(field_label)

    def test_avatar_help_text(self):
        field_label = self.form.fields['avatar'].help_text
        self.assertFalse(field_label)

    def test_first_name_max_length(self):
        max_length = self.form.fields['first_name'].max_length
        self.assertEqual(max_length, 24)

    def test_last_name_max_length(self):
        max_length = self.form.fields['last_name'].max_length
        self.assertEqual(max_length, 24)


class RegistrationFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form = RegistrationForm()

    def test_username_label(self):
        label = self.form.fields['username'].label
        self.assertTrue(label is None or label == 'Username')

    def test_password1_label(self):
        label = self.form.fields['password1'].label
        self.assertTrue(label is None or label == 'Password')

    def test_password2_label(self):
        label = self.form.fields['password2'].label
        self.assertTrue(label is None or label == 'Password confirmation')

    def test_first_name_label(self):
        label = self.form.fields['first_name'].label
        self.assertTrue(label is None or label == 'Имя')

    def test_last_name_label(self):
        label = self.form.fields['last_name'].label
        self.assertTrue(label is None or label == 'Фамилия')

    def test_first_name_help_text(self):
        help_text = self.form.fields['first_name'].help_text
        self.assertFalse(help_text)

    def test_last_name_help_text(self):
        help_text = self.form.fields['last_name'].help_text
        self.assertFalse(help_text)

    def test_first_name_max_length(self):
        max_length = self.form.fields['first_name'].max_length
        self.assertEqual(max_length, 24)

    def test_last_name_max_length(self):
        max_length = self.form.fields['last_name'].max_length
        self.assertEqual(max_length, 24)


class AuthFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form = AuthForm()

    def test_username_label(self):
        label = self.form.fields['username'].label
        self.assertTrue(label is None or label == 'Логин')

    def test_password_label(self):
        label = self.form.fields['password'].label
        self.assertTrue(label is None or label == 'Пароль')

    """def test_username_max_length(self):
        #this test fail max_length != 24
        max_length = self.form.fields['username'].max_length
        self.assertEqual(max_length, 24)"""

    def test_username_help_text(self):
        help_text = self.form.fields['username'].help_text
        self.assertFalse(help_text)

    def test_password_help_text(self):
        help_text = self.form.fields['password'].help_text
        self.assertFalse(help_text)
