from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class TestCore(TestCase):
    fixtures = ['ingredients_fixture.json']

    def setUp(self):
        self.user = User.objects.create_user(username="user", password="user")
        self.user.save()

    def test_client_index_page(self):
        """ GET on index page."""
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self):
        """ We can create an account on the site."""
        response = self.client.get(reverse('core:signup'))
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        """ We can log on site."""
        response = self.client.get(reverse('core:login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_page(self):
        """ We can logout on site."""
        response = self.client.get(reverse('core:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_signup_form(self):
        """ We can create an account on the site."""
        user_field = {
            'username': 'marron',
            'password1': 'cerise007',
            'password2': 'cerise007',
        }
        form = UserCreationForm(data=user_field)
        self.assert_(form.is_valid())
        user_marron = form.save()
        self.assertEqual(user_marron.username, "marron")

    def test_signup_post(self):
        """ We can create an account on the site."""
        user_field = {
            'username': 'marron',
            'password1': 'cerise007',
            'password2': 'cerise007',
        }
        response_post = self.client.post('/accounts/signup/', user_field)
        self.assertRedirects(response_post, '/')
        response = self.client.get('/')
        self.assertEqual(str(response.context['user']), user_field['username'])
        self.assertEqual(response.status_code, 200)

    def test_login_post(self):
        """ We can log on the site."""
        user_field = {
            'username': 'user',
            'password': 'user',
        }
        response_post = self.client.post('/accounts/login/', user_field)
        self.assertRedirects(response_post, '/')
        response = self.client.get('/')
        self.assertEqual(str(response.context['user']), 'user')
        self.assertEqual(response.status_code, 200)

    def test_logout_process(self):
        """ We can logout on site."""
        user_field = {
            'username': 'user',
            'password': 'user',
        }
        response_post = self.client.post('/accounts/login/', user_field)
        response = self.client.get('/')
        self.assertEqual(str(response.context['user']), 'user')
        self.client.get(reverse('core:logout'))
        response2 = self.client.get('/')
        self.assertEqual(str(response2.context['user']), 'AnonymousUser')
