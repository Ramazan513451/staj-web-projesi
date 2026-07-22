from django.urls import path
from auditlog import views

app_name = 'auditlog'

urlpatterns = [
    path('', views.audit_log_list, name='log_list'),
]
