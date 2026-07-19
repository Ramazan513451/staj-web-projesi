from django import forms
from django.utils.text import slugify
from .models import Page

class PageForm(forms.ModelForm):
    slug = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Boş bırakılırsa başlıktan otomatik üretilir'})
    )

    class Meta:
        model = Page
        fields = ['title', 'slug', 'content', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        title = self.cleaned_data.get('title')
        
        if not slug and title:
            # Replace Turkish characters for better slugs before slugify
            tr_map = {'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c', 'I': 'I', 'Ğ': 'G', 'Ü': 'U', 'Ş': 'S', 'Ö': 'O', 'Ç': 'C'}
            for tr, en in tr_map.items():
                title = title.replace(tr, en)
            slug = slugify(title)
            
        if not slug:
            raise forms.ValidationError("Slug alanı boş bırakılamaz ve başlıktan da üretilemedi.")
            
        qs = Page.objects.filter(slug=slug)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Bu URL adresi (slug) zaten başka bir sayfa tarafından kullanılıyor.")
            
        return slug
