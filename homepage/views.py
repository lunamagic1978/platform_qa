from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return HttpResponseRedirect('/index')
        else:
            ctx = {"error": "账号或者密码不正确"}
            return render(request, 'login.html', ctx)

    return render(request, 'index.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index')