from django.urls import path
from . import views

app_name = 'sliders'

urlpatterns = [
    path('', views.SliderListView.as_view(), name='list'),
    path('ekle/', views.SliderCreateView.as_view(), name='create'),
    path('<int:pk>/duzenle/', views.SliderUpdateView.as_view(), name='update'),
    path('<int:pk>/sil/', views.SliderDeleteView.as_view(), name='delete'),
]
