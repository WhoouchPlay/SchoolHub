from functools import wraps

from django.http import HttpRequest
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User

from Profile.models import Profile


def has_permission(action_name: str):
    def decorator(func):
        @wraps(func)
        def wrap_func(request: HttpRequest, *args, **kwargs):
            if Profile.objects.select_related("user").prefetch_related("positions_actions").filter(user__id=request.user.pk, positions__actions__name=action_name).exists():
            # if request.user.profile.positions.filter(actions__name=action_name).exists():
            # if User.objects.prefetch_related("profile", "profile__positions", "profile__positions__actions").filter(pk=request.user.pk, profile__positions__actions__name=action_name).exists():
                return func(request, *args, **kwargs)
            else:
                messages.error(request, "У Вас недостатньо прав 🤷")
                return redirect("resource")
        return wrap_func
    return decorator