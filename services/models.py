from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='services/')
    description = models.TextField()
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.image:
            from config.utils import optimize_image
            self.image = optimize_image(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
