from django.test import TestCase, Client
from django.urls import reverse, resolve, Resolver404
from .models import ContactMessage

class ContactMessageTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_empty_contact_form_submission(self):
        # Post empty data to contact form
        response = self.client.post('/iletisim/', {})
        
        # Should return 200 (redisplay form with errors)
        self.assertEqual(response.status_code, 200)
        
        # Verify no messages were created
        self.assertEqual(ContactMessage.objects.count(), 0)
        
        # Verify form has errors
        form = response.context['form']
        self.assertFormError(form, 'name', 'This field is required.')
        self.assertFormError(form, 'email', 'This field is required.')
        self.assertFormError(form, 'message', 'This field is required.')

    def test_no_delete_url_for_contact_message(self):
        # Try to resolve a hypothetical delete URL
        with self.assertRaises(Resolver404):
            resolve('/panel/messages/1/delete/')
            
        # Post to a hypothetical delete URL
        response = self.client.post('/panel/messages/1/delete/')
        self.assertEqual(response.status_code, 404)
        
        # Try to resolve another hypothetical delete URL
        with self.assertRaises(Resolver404):
            resolve('/panel/messages/delete/1/')
