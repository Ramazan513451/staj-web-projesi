from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from pages.models import Page
from sliders.models import Slider
from services.models import Service
from contactmessages.models import ContactMessage

def index(request):
    sliders = Slider.objects.filter(is_active=True).order_by('order')
    services = Service.objects.filter(is_featured=True).order_by('order')[:3]
    if not services.exists():
        services = Service.objects.all().order_by('-id')[:3]
        
    context = {
        'sliders': sliders,
        'services': services,
    }
    return render(request, 'index.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message
        )
        messages.success(request, 'Mesajınız başarıyla alınmıştır. En kısa sürede dönüş yapılacaktır.')
        return redirect('contact')
        
    return render(request, 'contact.html')

def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    return render(request, 'page_detail.html', {'page': page})

