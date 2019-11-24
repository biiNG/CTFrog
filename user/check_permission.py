from django.shortcuts import render
from django.contrib import auth
from django.shortcuts import redirect
from .models import User
from .testing import *


def check_login(function):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """

    def deco(*args, **kargs):
        request = args[0]
        # writetest(args)
        # writetest(kargs)

        if request.session.get('is_login', None):
            request.session['message'] = '请先登录'
            return redirect('user:login')

        else:
            return function(request, **kargs)

    return deco


def check_admin(function):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """

    def deco(*args, **kargs):
        request = args[0]
        # writetest(args)
        # writetest(kargs)

        user = User.objects.get(name=request.session['username'])
        if not user.issuperuser:
            request.session['message'] = '权限不够！'
            return redirect('user:teamprofile')
        else:
            return function(request, **kargs)

    return deco
