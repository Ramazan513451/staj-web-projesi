from django.test import TestCase, Client
from django.urls import reverse

class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_unauthenticated_user_redirected_from_panel(self):
        # '/panel/dashboard/' or '/panel/pages/' should redirect to login
        # '/panel/' itself might be redirected to login if it exists
        # Let's test accessing dashboard
        response = self.client.get('/panel/dashboard/')
        
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/panel/login/' in response.url)
        
        # Direct hit to pages list
        response_pages = self.client.get('/panel/pages/')
        self.assertEqual(response_pages.status_code, 302)
        self.assertTrue('/panel/login/' in response_pages.url)
