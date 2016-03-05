from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST,require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from .models import MyUser

# Create your views here.
def hello(request):
    return HttpResponse('<h1>Hello</h1>');

@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated():
        return redirect(reverse('home', kwargs={'id': request.user.id}));
    if request.method == 'GET':
        context = { 'f' : LoginForm()};
        return render(request, 'account/auth/login.html', context);
    else:
        f = LoginForm(request.POST);
        if not f.is_valid():
            return render(request, 'account/auth/login.html', {'f' : f});
        else:
            user = f.authenticated_user
            auth_login(request, user)
            return redirect(reverse('home', kwargs={'id': user.id}));

@require_GET
@login_required
def home(request, id):
    return render(request, 'account/auth/loggedin.html')

def logout(request):
    auth_logout(request)
    return redirect(reverse('login'));

