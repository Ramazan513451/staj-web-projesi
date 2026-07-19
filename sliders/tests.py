from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Slider

class SliderValidationTests(TestCase):
    def test_max_5_active_sliders(self):
        # Create a dummy image
        dummy_image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        
        # Create 5 active sliders
        for i in range(5):
            slider = Slider(title=f'Slider {i}', is_active=True, image=dummy_image)
            slider.full_clean() # Should not raise
            slider.save()
            
        # Try to create 6th active slider
        slider_6 = Slider(title='Slider 6', is_active=True, image=dummy_image)
        with self.assertRaisesMessage(ValidationError, "En fazla 5 aktif slider olabilir."):
            slider_6.full_clean()
            
    def test_more_than_5_inactive_sliders_allowed(self):
        # Create a dummy image
        dummy_image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        
        # Create 5 active sliders
        for i in range(5):
            Slider.objects.create(title=f'Slider {i}', is_active=True, image=dummy_image)
            
        # Should be able to create an inactive slider
        slider_inactive = Slider(title='Inactive Slider', is_active=False, image=dummy_image)
        slider_inactive.full_clean() # Should not raise
        slider_inactive.save()
        self.assertEqual(Slider.objects.count(), 6)
