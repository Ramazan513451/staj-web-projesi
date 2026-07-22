from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from auditlog.models import ActivityLog

@login_required(login_url='/panel/login/')
def audit_log_list(request):
    if not (hasattr(request.user, 'profile') and request.user.profile.role == 'admin'):
        raise PermissionDenied
    logs = ActivityLog.objects.all()
    return render(request, 'auditlog/log_list.html', {'logs': logs})
