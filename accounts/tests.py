from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

from .forms import ProfileForm


class AccountsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='setUpUser@gmail.com', username='setUpUser',
                                                         password='12345')

    def test_profile_form(self):
        form = ProfileForm(instance=self.user, data={
            'first_name': 'firstName',
            'last_name': 'lastName',
            'bio': 'bio',
            'username': 'username',
        })

        self.assertTrue(form.is_valid())

    def test_login_required_profile_view(self):
        self.client.logout()
        response = self.client.get(reverse('account_profile'))

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'account/profile.html')

    def test_profile_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('account_profile'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/profile.html')

    def test_profile_view_post_method(self):
        self.client.force_login(self.user)
        data = {
            'first_name': 'testFirstName',
            'last_name': 'testLastName',
            'bio': 'testBio',
            'username': 'testUsername',
            'email': 'testEmail@gmail.com',
        }
        response = self.client.post(reverse('account_profile'), data=data)

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.first_name, data.get('first_name'))
        self.assertEqual(self.user.last_name, data.get('last_name'))
        self.assertEqual(self.user.bio, data.get('bio'))
        self.assertEqual(self.user.username, data.get('username'))
        # Normal user cannot change the email
        self.assertNotEqual(self.user.email, data.get('email'))

    def test_profile_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('account_profile'))

        self.assertContains(response, 'پروفایل من')

    def test_profile_url(self):
        self.client.force_login(self.user)
        response = self.client.get('/accounts/profile/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/profile.html')

    def test_subscription_login_required(self):
        self.client.logout()
        response = self.client.get(reverse('account_subscription'))

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'account/subscription.html')

    def test_subscription_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('account_subscription'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/subscription.html')
        self.assertContains(response, 'اشتراک من')

    def test_subscription_url(self):
        self.client.force_login(self.user)
        response = self.client.get('/accounts/subscription/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/subscription.html')
