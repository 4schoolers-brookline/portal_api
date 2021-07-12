from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Parent

def index(request):
    context = {}
    if (request.user.is_authenticated):
        context['parent'] = Parent.objects.get(user = request.user)
        return redirect('parent_highlights')
    else:
        return redirect('parent_login')


def login(request):
    # TODO: check if authenticated by other account type
    context = {}
    if (request.user.is_authenticated):
        return redirect('parent_profile')

    if (request.method == 'POST'):
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email = email)
        except:
            context['invalid'] = True
            return render(request, 'parent/login.jinja', context)

        if (user.check_password(password)):
            auth.login(request, user)
            return redirect('parent_profile')
        else:
            context['invalid'] = True
            return render(request, 'parent/login.jinja', context)

    return render(request, 'parent/login.jinja', context)

@login_required
def profile(request):
    context = {}
    

    return render(request, 'parent/profile.jinja', context)

@login_required
def highlights(request):
    context = {}
    

    return render(request, 'parent/highlights.jinja', context)

