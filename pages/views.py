from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Page
from .forms import PageForm
from sliders.models import Slider
from services.models import Service
from contactmessages.models import ContactMessage
from contactmessages.forms import ContactForm

class PageListView(LoginRequiredMixin, ListView):
    model = Page
    template_name = 'pages/page_list.html'
    context_object_name = 'pages'
    ordering = ['-created_at']

class PageCreateView(LoginRequiredMixin, CreateView):
    model = Page
    form_class = PageForm
    template_name = 'pages/page_form.html'
    success_url = reverse_lazy('pages:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Sayfa başarıyla eklendi.')
        return super().form_valid(form)

class PageUpdateView(LoginRequiredMixin, UpdateView):
    model = Page
    form_class = PageForm
    template_name = 'pages/page_form.html'
    success_url = reverse_lazy('pages:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Sayfa başarıyla güncellendi.')
        return super().form_valid(form)

class PageDeleteView(LoginRequiredMixin, DeleteView):
    model = Page
    template_name = 'panel/delete_confirm.html'
    success_url = reverse_lazy('pages:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('pages:list')
        return context
        
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Sayfa başarıyla silindi.')
        return super().delete(request, *args, **kwargs)

from sliders.models import Slider
from services.models import Service

# Public Views
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
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save(commit=False)
            contact_message.status = 'new'
            contact_message.save()
            messages.success(request, 'Mesajınız başarıyla alınmıştır. En kısa sürede size dönüş yapacağız.')
            return redirect('contact')
    else:
        form = ContactForm()
        
    context = {
        'form': form
    }
    return render(request, 'contact.html', context)

def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    return render(request, 'page_detail.html', {'page': page})
