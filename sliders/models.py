from django.db import models
from django.core.exceptions import ValidationError

class Slider(models.Model):
    image = models.ImageField(upload_to='sliders/')
    title = models.CharField(max_length=255, blank=True)
    subtitle = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    def clean(self):
        if self.is_active:
            active_count = Slider.objects.filter(is_active=True).exclude(pk=self.pk).count()
            if active_count >= 5:
                raise ValidationError("En fazla 5 aktif slider olabilir.")
        super().clean()

    def save(self, *args, **kwargs):
        if self.image:
            from config.utils import optimize_image
            self.image = optimize_image(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title if self.title else f"Slider {self.id}"
