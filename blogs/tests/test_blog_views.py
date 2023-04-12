from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from app_blogs.models import Blog, Entry


class CreateBlogViewTest(TestCase):
    """ Tests for CreateBlogView """
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='testUser_4',
                                                       password='1X<ISRUkw+tuK',
                                                       first_name='Name', last_name='Surname')
        cls.url_name = 'create-blog'
        cls.url = '/blogs/create/'

    def setUp(self) -> None:
        self.client.login(username='testUser_4', password='1X<ISRUkw+tuK')

    def test_url_exists_at_correct_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_blogs/new-blog.html')

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/users/login/?next={self.url}')

    def test_post_correct_data(self):
        post_data = {'name': 'blog_name',
                     'tags': 'tag1, tag2'}
        response = self.client.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blog-list'))
        blog = Blog.objects.first()
        self.assertEqual(str(blog), 'blog_name')

    def test_post_incorrect_data(self):
        post_data = {'name': 'incorrect_blog'}
        response = self.client.post(self.url, data=post_data)
        self.assertNotEqual(response.status_code, 302)
        blog = Blog.objects.first()
        self.assertEqual(str(blog), 'None')


class BlogListViewTest(TestCase):
    """ Tests for BlogListView """
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='testUser_4',
                                                       password='1X<ISRUkw+tuK',
                                                       first_name='Name', last_name='Surname')
        cls.url_name = 'blog-list'
        cls.url = '/blogs/list/'

    def setUp(self) -> None:
        self.client.login(username='testUser_4', password='1X<ISRUkw+tuK')

    def test_url_exists_at_correct_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_blogs/blog_list.html')

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/users/login/?next={self.url}')

    def test_get_queryset(self):
        Blog.objects.create(user=self.user, name='first_blog', tags='tag1')
        Blog.objects.create(user=self.user, name='second_blog', tags='tag2')
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['blog_list'])
        self.assertEqual(len(response.context['blog_list']), 2)


class BlogEditViewTest(TestCase):
    """ Tests for BlogEditView """
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='testUser_4',
                                                       password='1X<ISRUkw+tuK',
                                                       first_name='Name', last_name='Surname')
        blog = Blog.objects.create(user=cls.user, name='first_blog', tags='tag1')
        cls.pk = blog.id
        cls.url = f'/blogs/edit/{cls.pk}/'
        cls.url_name = 'blog-edit'

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
        self.assertTemplateUsed(response, 'app_blogs/blog_edit.html')

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/users/login/?next={self.url}')

    def test_post_correct_data(self):
        post_data = {'name': 'second_blog',
                     'tags': 'tag2'}
        response = self.client.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blog-list'))
        blog = Blog.objects.first()
        self.assertEqual(str(blog), 'second_blog')

    def test_post_incorrect_data(self):
        post_data = {'name': 'second_blog',
                     'tags': ''}
        response = self.client.post(self.url, data=post_data)
        self.assertNotEqual(response.status_code, 302)
        blog = Blog.objects.first()
        self.assertNotEqual(str(blog), 'second_blog')


class BlogDetailViewTest(TestCase):
    """ Tests for BlogDetailView """
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='testUser_4',
                                                       password='1X<ISRUkw+tuK',
                                                       first_name='Name', last_name='Surname')
        blog = Blog.objects.create(user=cls.user, name='first_blog', tags='tag1')
        cls.pk = blog.id
        cls.url_name = 'entry-list'
        cls.url = f'/blogs/detail/{cls.pk}/'

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
        self.assertTemplateUsed(response, 'app_blogs/entry_list.html')

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/users/login/?next={self.url}')

    def test_get_context_without_entry(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['blog'])
        self.assertFalse(response.context['entry_list'])

    def test_get_context_with_entry(self):
        blog = Blog.objects.first()
        for i in range(1, 6):
            Entry.objects.create(blog=blog, title=f'title{i}', body_text=f'text{i}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['blog'])
        self.assertTrue(response.context['entry_list'])
        self.assertEqual(len(response.context['entry_list']), 5)
