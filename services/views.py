from django.shortcuts import render

from .models import Service

def service_list(request):
    services = Service.objects.all().order_by('order')
    return render(request, 'services.html', {'services': services})
