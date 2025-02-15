from functools import wraps
from django.http import HttpResponseRedirect
from django.contrib import messages

def members_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_member or request.user.is_staff or request.user.is_superuser):
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'You must a member to access this page')
            return HttpResponseRedirect('/members/login')
    return _wrapped_view