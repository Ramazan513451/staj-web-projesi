from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.decorators import role_required
from .models import SiteSettings
from .forms import SiteSettingsForm

@role_required('admin')
def settings_view(request):
    instance = SiteSettings.objects.first()
    
    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Genel ayarlar başarıyla güncellendi.')
            return redirect('sitesettings:settings')
        else:
            messages.error(request, 'Lütfen formdaki hataları düzeltin.')
    else:
        form = SiteSettingsForm(instance=instance)
        
    return render(request, 'sitesettings/settings.html', {'form': form})
