from django.db import models

class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('new', 'Yeni'),
        ('read', 'Okundu'),
        ('archived', 'Arşivlendi'),
    ]
    name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(blank=False)
    phone = models.CharField(max_length=50, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"
