from functools import wraps
from django.shortcuts import redirect


def handle_authenticated_user(view_func):
    """Decorator that handles authenticated users (restrict access to the 'sign up', 'login', etc.)"""

    @wraps(view_func)
    def wrapper_func(view, *args, **kwargs):
        if view.request.user.is_authenticated:
            return redirect('/posts/')
        else:
            return view_func(view, *args, **kwargs)

    return wrapper_func




