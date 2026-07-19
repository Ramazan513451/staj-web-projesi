from django.test import TestCase, Client
from django.contrib.auth.models import User
from accounts.models import Profile

class SiteSettingsAuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create editor user
        self.editor_user = User.objects.create_user(username='editor', password='password123')
        self.editor_profile, _ = Profile.objects.get_or_create(user=self.editor_user)
        self.editor_profile.role = 'editor'
        self.editor_profile.save()
        
        # Create admin user
        self.admin_user = User.objects.create_user(username='admin', password='password123')
        self.admin_profile, _ = Profile.objects.get_or_create(user=self.admin_user)
        self.admin_profile.role = 'admin'
        self.admin_profile.save()

    def test_editor_access_settings_forbidden(self):
        self.client.login(username='editor', password='password123')
        response = self.client.get('/panel/settings/')
        self.assertEqual(response.status_code, 403)

    def test_admin_access_settings_allowed(self):
        self.client.login(username='admin', password='password123')
        response = self.client.get('/panel/settings/')
        self.assertEqual(response.status_code, 200)
