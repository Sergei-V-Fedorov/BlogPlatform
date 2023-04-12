import urllib
import os.path
from django.test import TestCase
from app_blogs.models import Entry, Blog, File
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile


class EntryCreateViewTest(TestCase):
    """ Tests for EntryCreateView """

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='testUser_4',
                                                        password='1X<ISRUkw+tuK',
                                                        first_name='Name', last_name='Surname')
        blog = Blog.objects.create(user=cls.user, name='first_blog', tags='tag1')
        cls.pk = blog.id
        cls.url_name = 'create-entry'
        cls.url = f'/blogs/entry/{cls.pk}/create/'

    def setUp(self) -> None:
        self.client.login(username='testUser_4', password='1X<ISRUkw+tuK')

    def test_url_exists_at_correct_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse(self.url_name, args=[self.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'])

    def test_template_name_correct(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_blogs/new_entry.html')

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/users/login/?next={self.url}')

    def test_post_correct_data_without_file(self):
        post_data = {'title': 'title1',
                     'body_text': 'text1'}
        response = self.client.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('entry-list', args=[self.pk]))
        entry = Entry.objects.first()
        self.assertEqual(str(entry), 'title1')

    def test_post_incorrect_data(self):
        post_data = {'title': '', 'body_text': ''}
        response = self.client.post(self.url, data=post_data)
        self.assertNotEqual(response.status_code, 302)
        entry = Entry.objects.first()
        self.assertEqual(str(entry), 'None')

    def test_post_data_with_images(self):
        # read a list of images
        file_dir = './app_blogs/tests/'
        file_list = [file_name
                     for file_name in os.listdir(file_dir)
                     if file_name.endswith('.png')]
        # uploaded images
        file_data = []
        for file_name in file_list:
            img = open(os.path.join(file_dir, file_name), 'rb')
            file_data.append(SimpleUploadedFile(file_name, img.read()))
        # past data
        post_data = {'title': 'title1', 'body_text': 'text1',
                     'file': file_data, 'description': 'image1'}
        response = self.client.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('entry-list', args=[self.pk]))
        entry = Entry.objects.first()
        file = entry.files.all()
        self.assertEqual(str(entry), 'title1')
        self.assertEqual(str(file[0]), 'image1')
        self.assertEqual(len(file), len(file_list))


class EntryDetailViewTest(TestCase):
    """ Tests for EntryDetailView """
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='testUser_4',
                                                        password='1X<ISRUkw+tuK',
                                                        first_name='Name', last_name='Surname')
        blog = Blog.objects.create(user=cls.user, name='first_blog', tags='tag1')
        entry = Entry.objects.create(blog=blog, title='entry_title', body_text='entry_text')
        cls.pk = entry.id
        cls.url_name = 'detail-entry'
        cls.url = f'/blogs/entry/{cls.pk}/'

    def setUp(self) -> None:
        self.client.login(username='testUser_4', password='1X<ISRUkw+tuK')

    def test_url_exists_at_correct_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse(self.url_name, args=[self.pk]))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_blogs/entry_detail.html')

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/users/login/?next={self.url}')

    def test_get_context_without_files(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['entry'])
        self.assertFalse(response.context['files'])

    def test_get_context_with_files(self):
        entry = Entry.objects.first()
        # add 2 files to entry
        File.objects.create(entry=entry, file='files/dasha.png',
                            description='entry_images')
        File.objects.create(entry=entry, file='files/test.png',
                            description='entry_images')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['entry'])
        self.assertTrue(response.context['files'])
        self.assertEqual(len(response.context['files']), len(entry.files.all()))


class EntryEditViewTest(TestCase):
    """ Tests for EntryEditView """
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='testUser_4',
                                                       password='1X<ISRUkw+tuK',
                                                       first_name='Name', last_name='Surname')
        blog = Blog.objects.create(user=cls.user, name='first_blog', tags='tag1')
        entry = Entry.objects.create(blog=blog, title='entry_title', body_text='entry_text')
        cls.pk = entry.id
        cls.url_name = 'edit-entry'
        cls.url = f'/blogs/entry/{cls.pk}/edit/'

    def setUp(self) -> None:
        self.client.login(username='testUser_4', password='1X<ISRUkw+tuK')

    def test_url_exists_at_correct_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse(self.url_name, args=[self.pk]))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_blogs/entry_edit.html')

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/users/login/?next={self.url}')

    def test_post_correct_data_without_images(self):
        post_data = {'title': 'new_title',
                     'body_text': 'new_text'}
        response = self.client.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('detail-entry', args=[self.pk]))
        entry = Entry.objects.first()
        self.assertEqual(str(entry), 'new_title')

    def test_post_incorrect_data(self):
        post_data = {'title': '', 'body_text': ''}
        response = self.client.post(self.url, data=post_data)
        self.assertNotEqual(response.status_code, 302)
        entry = Entry.objects.first()
        self.assertEqual(str(entry), 'entry_title')

    def test_post_data_with_images(self):
        # read a list of images
        file_dir = './app_blogs/tests/'
        file_list = [file_name
                     for file_name in os.listdir(file_dir)
                     if file_name.endswith('.png')]
        # uploaded images
        file_data = []
        for file_name in file_list:
            img = open(os.path.join(file_dir, file_name), 'rb')
            file_data.append(SimpleUploadedFile(file_name, img.read()))
        # past data
        post_data = {'title': 'new_title', 'body_text': 'new_text',
                     'file': file_data, 'description': 'new_images'}
        response = self.client.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('detail-entry', args=[self.pk]))
        entry = Entry.objects.first()
        file = entry.files.all()
        self.assertEqual(str(entry), 'new_title')
        self.assertEqual(str(file[0]), 'new_images')
        self.assertEqual(len(file), len(file_list))


class MainPageViewTest(TestCase):
    """ Tests for MainPageView """
    @classmethod
    def setUpTestData(cls):
        cls.url_name = 'main'
        cls.url = '/blogs/'

    def test_url_exists_at_correct_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_blogs/entry_all.html')

    def test_get_queryset(self):
        # create entries
        for u in range(1, 3):
            user = get_user_model().objects.create_user(username=f'testUser{u}',
                                                        password='1X<ISRUkw+tuK',
                                                        first_name=f'Name{u}',
                                                        last_name=f'Surname{u}')
            blog = Blog.objects.create(user=user, name=f'blog of {user.username}',
                                       tags='tag')
            for e in range(1, 3):
                Entry.objects.create(blog=blog, title=f'entry{e}_title',
                                     body_text=f'entry{e}_text')
        entry_count = Entry.objects.all().count()
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['entry_list'])
        self.assertEqual(len(response.context['entry_list']), entry_count)


class UploadEntryFromFileTest(TestCase):
    """ Tests for upload_entry_from_file """
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='testUser_4',
                                                       password='1X<ISRUkw+tuK',
                                                       first_name='Name', last_name='Surname')
        blog = Blog.objects.create(user=cls.user, name='first_blog', tags='tag1')
        cls.pk = blog.id
        cls.url_name = 'upload-entry'
        cls.url = f'/blogs/detail/{cls.pk}/upload/'

    def setUp(self) -> None:
        self.client.login(username='testUser_4', password='1X<ISRUkw+tuK')

    def test_url_exists_at_correct_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse(self.url_name, args=[self.pk]))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_blogs/upload_entry_file.html')

    def test_post_correct_data(self):
        file_dir = './app_blogs/tests/'
        # add 2 entries from file
        file_name = 'entry.csv'
        file = open(os.path.join(file_dir, file_name), 'rb')
        file_data = SimpleUploadedFile(file_name, file.read())
        post_data = {'file': file_data}
        response = self.client.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('entry-list', args=[self.pk]))
        entries = Entry.objects.all().count()
        self.assertEqual(entries, 2)
