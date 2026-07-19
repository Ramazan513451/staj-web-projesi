from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.models import Profile
from .models import Service
from contactmessages.models import ContactMessage

class IntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create admin user
        self.admin_user = User.objects.create_user(username='admin', password='password123')
        self.admin_profile, _ = Profile.objects.get_or_create(user=self.admin_user)
        self.admin_profile.role = 'admin'
        self.admin_profile.save()
        
        # Create a valid dummy image for service
        import io
        from PIL import Image
        img = Image.new('RGB', (100, 100), color=(73, 109, 137))
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        self.dummy_image = SimpleUploadedFile(name='test_service.jpg', content=img_byte_arr.read(), content_type='image/jpeg')

    def test_end_to_end_service_creation_and_homepage_display(self):
        # 1. Login as admin
        self.client.login(username='admin', password='password123')
        
        # 2. Create a new service from panel (is_featured=True)
        # Assuming the create URL is 'services:create' i.e. /panel/services/create/
        post_data = {
            'title': 'Otomatik Test Hizmeti',
            'description': 'Bu hizmet entegrasyon testi ile oluşturulmuştur.',
            'is_featured': True,
            'order': 1,
            'image': self.dummy_image
        }
        response_create = self.client.post('/panel/services/ekle/', post_data)
        
        # Check if creation redirected successfully
        if response_create.status_code != 302:
            print("FORM ERRORS:", response_create.context['form'].errors)
        self.assertEqual(response_create.status_code, 302)
        self.assertTrue(Service.objects.filter(title='Otomatik Test Hizmeti').exists())
        
        # 3. Fetch public homepage
        response_home = self.client.get('/')
        self.assertEqual(response_home.status_code, 200)
        
        # 4. Verify new service title is in homepage
        self.assertContains(response_home, 'Otomatik Test Hizmeti')
        self.assertContains(response_home, 'Bu hizmet entegrasyon testi ile oluşturulmuştur.')

    def test_message_archive_does_not_delete(self):
        # 1. Login as admin
        self.client.login(username='admin', password='password123')
        
        # 2. Create a message
        msg = ContactMessage.objects.create(
            name='Test User',
            email='test@example.com',
            message='Test message',
            status='new'
        )
        
        # 3. Archive the message
        response_archive = self.client.post(f'/panel/messages/{msg.pk}/archive/')
        self.assertEqual(response_archive.status_code, 302)
        
        # 4. Verify message still exists and status is archived
        msg.refresh_from_db()
        self.assertEqual(msg.status, 'archived')
        self.assertTrue(ContactMessage.objects.filter(pk=msg.pk).exists())
