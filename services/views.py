from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Service
from .forms import ServiceForm

class ServiceListView(LoginRequiredMixin, ListView):
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'
    ordering = ['order']

class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'services/service_form.html'
    success_url = reverse_lazy('services:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Hizmet başarıyla eklendi.')
        return super().form_valid(form)

class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'services/service_form.html'
    success_url = reverse_lazy('services:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Hizmet başarıyla güncellendi.')
        return super().form_valid(form)

class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Service
    template_name = 'panel/delete_confirm.html'
    success_url = reverse_lazy('services:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('services:list')
        return context
        
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Hizmet başarıyla silindi.')
        return super().delete(request, *args, **kwargs)

from django.shortcuts import render

def service_list(request):
    services = Service.objects.all().order_by('order')
    return render(request, 'services.html', {'services': services})
