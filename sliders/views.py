from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Slider
from .forms import SliderForm

class SliderListView(LoginRequiredMixin, ListView):
    model = Slider
    template_name = 'sliders/slider_list.html'
    context_object_name = 'sliders'
    ordering = ['order']

class SliderCreateView(LoginRequiredMixin, CreateView):
    model = Slider
    form_class = SliderForm
    template_name = 'sliders/slider_form.html'
    success_url = reverse_lazy('sliders:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Slider başarıyla eklendi.')
        return super().form_valid(form)

class SliderUpdateView(LoginRequiredMixin, UpdateView):
    model = Slider
    form_class = SliderForm
    template_name = 'sliders/slider_form.html'
    success_url = reverse_lazy('sliders:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Slider başarıyla güncellendi.')
        return super().form_valid(form)

class SliderDeleteView(LoginRequiredMixin, DeleteView):
    model = Slider
    template_name = 'panel/delete_confirm.html'
    success_url = reverse_lazy('sliders:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('sliders:list')
        return context
        
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Slider başarıyla silindi.')
        return super().delete(request, *args, **kwargs)
