from django.db import models
from django.contrib.auth.models import User

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    entity_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        user_str = self.user.username if self.user else "Anonim/Bilinmeyen"
        return f"{user_str} - {self.action} on {self.entity_name} at {self.created_at}"
    
    class Meta:
        ordering = ['-created_at']
