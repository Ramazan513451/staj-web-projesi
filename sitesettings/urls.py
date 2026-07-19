from django.urls import path
from . import views

app_name = 'sitesettings'

urlpatterns = [
    path('', views.settings_view, name='settings'),
]
