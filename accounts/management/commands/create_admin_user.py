from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
import getpass

class Command(BaseCommand):
    help = 'Creates a super admin user with Profile role=admin'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("--- Süper Admin Kullanıcısı Oluşturma ---"))
        
        username = input("Kullanıcı adı: ")
        while User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f"Hata: '{username}' zaten kullanımda."))
            username = input("Kullanıcı adı: ")
            
        password = getpass.getpass("Şifre: ")
        password_confirm = getpass.getpass("Şifre (Tekrar): ")
        
        while password != password_confirm or not password:
            self.stdout.write(self.style.ERROR("Hata: Şifreler eşleşmiyor veya boş olamaz."))
            password = getpass.getpass("Şifre: ")
            password_confirm = getpass.getpass("Şifre (Tekrar): ")
            
        try:
            with transaction.atomic():
                # email is empty because we don't strictly require it
                user = User.objects.create_superuser(username=username, email='', password=password)
                
                # The signal will automatically create a Profile with role='editor'
                # We need to update it to 'admin'
                user.profile.role = 'admin'
                user.profile.save()
            
            self.stdout.write(self.style.SUCCESS(f"Süper admin kullanıcısı '{username}' başarıyla oluşturuldu!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Hata oluştu: {e}"))
