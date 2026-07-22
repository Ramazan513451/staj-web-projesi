from django.db.models.signals import post_save, post_delete
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from auditlog.models import ActivityLog
from auditlog.middleware import get_current_request, get_client_ip
from sitesettings.models import SiteSettings
from services.models import Service
from pages.models import Page
from sliders.models import Slider
from contactmessages.models import ContactMessage

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ActivityLog.objects.create(
        user=user,
        action="Başarılı Giriş",
        entity_name="Auth",
        ip_address=get_client_ip(request) if request else None
    )

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    ActivityLog.objects.create(
        user=user,
        action="Çıkış Yapıldı",
        entity_name="Auth",
        ip_address=get_client_ip(request) if request else None
    )

@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    ActivityLog.objects.create(
        user=None,
        action=f"Başarısız Giriş Denemesi ({credentials.get('username', '')})",
        entity_name="Auth",
        ip_address=get_client_ip(request) if request else None
    )

def log_model_change(sender, instance, action, **kwargs):
    request = get_current_request()
    user = getattr(request, 'user', None) if request else None
    if user and not user.is_authenticated:
        user = None
    ip_address = get_client_ip(request) if request else None
    entity_name = sender.__name__

    ActivityLog.objects.create(
        user=user,
        action=action,
        entity_name=entity_name,
        ip_address=ip_address
    )

@receiver(post_save, sender=SiteSettings)
@receiver(post_save, sender=Service)
@receiver(post_save, sender=Page)
@receiver(post_save, sender=Slider)
@receiver(post_save, sender=ContactMessage)
def log_post_save(sender, instance, created, **kwargs):
    action = f"{sender.__name__} Eklendi" if created else f"{sender.__name__} Güncellendi"
    log_model_change(sender, instance, action)

@receiver(post_delete, sender=SiteSettings)
@receiver(post_delete, sender=Service)
@receiver(post_delete, sender=Page)
@receiver(post_delete, sender=Slider)
@receiver(post_delete, sender=ContactMessage)
def log_post_delete(sender, instance, **kwargs):
    action = f"{sender.__name__} Silindi"
    log_model_change(sender, instance, action)
