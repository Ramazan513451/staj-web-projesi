from .models import Page

def published_pages(request):
    pages = Page.objects.filter(is_published=True).order_by('title')
    return {'published_pages': pages}
