from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from services.models import Service
from pages.models import Page
from contactmessages.models import ContactMessage

@login_required(login_url='/panel/login/')
def dashboard(request):
    total_services = Service.objects.count()
    total_pages = Page.objects.count()
    total_messages = ContactMessage.objects.count()
    new_messages = ContactMessage.objects.filter(status='new').count()
    
    context = {
        'total_services': total_services,
        'total_pages': total_pages,
        'total_messages': total_messages,
        'new_messages': new_messages,
    }
    return render(request, 'dashboard/index.html', context)
