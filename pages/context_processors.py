from .models import Page

def custom_pages(request):
    """
    Tüm sayfalarda menü vb. yerlerde dinamik sayfaları göstermek için
    yayında olan sayfaları (is_published=True) döndürür.
    """
    return {
        'menu_pages': Page.objects.filter(is_published=True).order_by('created_at')
    }
