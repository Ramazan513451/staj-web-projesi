"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from pages import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("iletisim/", views.contact, name="contact"),
    path("sayfa/<slug:slug>/", views.page_detail, name="page_detail"),
    path("panel/", include("accounts.urls")),
    path("panel/dashboard/", include("dashboard.urls")),
    path("panel/settings/", include("sitesettings.urls")),
    path("panel/services/", include("services.urls")),
    path("panel/pages/", include("pages.urls")),
    path("panel/sliders/", include("sliders.urls")),
    path("panel/messages/", include("contactmessages.urls")),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
