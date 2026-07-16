from django.db import models

class SiteSettings(models.Model):
    site_title = models.CharField(max_length=255, blank=False)
    logo = models.ImageField(upload_to='logos/', blank=False)
    primary_color = models.CharField(max_length=7, default='#1a73e8')
    address = models.TextField(blank=False)
    phone = models.CharField(max_length=50, blank=False)
    email = models.EmailField(blank=False)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    map_iframe = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if SiteSettings.objects.exists() and not self.pk:
            self.pk = SiteSettings.objects.first().pk
        super().save(*args, **kwargs)

    def __str__(self):
        return self.site_title if self.site_title else "Genel Ayarlar"
