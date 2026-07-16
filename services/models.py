from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='services/')
    description = models.TextField()
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
