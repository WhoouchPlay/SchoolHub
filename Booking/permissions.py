from functools import wraps

from django.http import HttpRequest
from django.contrib import messages
from django.shortcuts import redirect



def has_permission(action_name: str):
    def decorator(func):
        @wraps(func)
        def wrap_func(request: HttpRequest, *args, **kwargs):
            if request.user.profile.positions.filter(actions__name=action_name).exists():
                return func(request, *args, **kwargs)
            else:
                messages.error(request, "У Вас недостатньо прав 🤷")
                return redirect("resource")
        return wrap_func
    return decorator