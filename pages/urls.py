from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.PageListView.as_view(), name='list'),
    path('ekle/', views.PageCreateView.as_view(), name='create'),
    path('<int:pk>/duzenle/', views.PageUpdateView.as_view(), name='update'),
    path('<int:pk>/sil/', views.PageDeleteView.as_view(), name='delete'),
]
