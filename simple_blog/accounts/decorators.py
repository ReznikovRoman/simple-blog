from functools import wraps

from django.shortcuts import redirect, reverse


def restrict_authenticated_users(view_func):
    """Decorator that handles authenticated users (restrict access to the 'sign up', 'login', etc.)."""

    @wraps(view_func)
    def wrapper_func(view, *args, **kwargs):
        if view.request.user.is_authenticated:
            return redirect(reverse('posts:all'))
        else:
            return view_func(view, *args, **kwargs)

    return wrapper_func
