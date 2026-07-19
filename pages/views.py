from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Page
from .forms import PageForm

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

# Public Views
def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')
