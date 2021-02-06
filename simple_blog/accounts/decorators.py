
from functools import wraps

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect


################################################################################################################


def unauthenticated_user(view_func):
    @wraps(view_func)
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/posts/')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func




