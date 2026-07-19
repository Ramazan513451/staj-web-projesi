from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from functools import wraps

def role_required(allowed_roles):
    """
    allowed_roles can be a single role string or a list of roles.
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url='/panel/login/')
        def _wrapped_view(request, *args, **kwargs):
            roles = [allowed_roles] if isinstance(allowed_roles, str) else allowed_roles
            
            # Check if user has a profile and role is allowed
            if hasattr(request.user, 'profile') and request.user.profile.role in roles:
                return view_func(request, *args, **kwargs)
                
            raise PermissionDenied
        return _wrapped_view
    return decorator
