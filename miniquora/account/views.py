from django.shortcuts import render, get_object_or_404, redirect
from  django.core import serializers
from django.http import Http404, JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST,require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.template import loader
from .forms import LoginForm, ForgotPassword, SetPasswordForm, SignupForm
from .models import MyUser, create_otp, get_valid_otp_object

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
            return JsonResponse({ 'errors' : f.errors})
        else:
            user = f.authenticated_user
            auth_login(request, user)
            return JsonResponse({'status' : 1 })
def forgot_password(request):
    if request.user.is_authenticated():
        return redirect(reverse('home', kwargs={'id': request.user.id}));
    if request.method == 'GET':
        context = { 'f' : ForgotPassword()};
        return render(request, 'account/auth/forgot_password.html', context);
    else:
        f = ForgotPassword(request.POST);
        if not f.is_valid():
            return render(request, 'account/auth/forgot_password.html', {'f' : f});
        else:
            user = MyUser.objects.get(username = f.cleaned_data['username'])
            otp = create_otp(user = user, purpose = 'FP')
            email_body_context = { 'u' : user, 'otp' : otp}
            body = loader.render_to_string('account/auth/email/forgot_password.txt', email_body_context)
            message = EmailMultiAlternatives("Reset Password", body, settings.EMAIL_HOST_USER, [user.email])
            #message.attach_alternative(html_body, 'text/html')
            message.send()
            return render(request, 'account/auth/forgot_email_sent.html', {'u': user});

def reset_password(request, id = None, otp = None):
    if request.user.is_authenticated():
        return redirect(reverse('home', kwargs={'id': request.user.id}));
    user = get_object_or_404(MyUser, id=id);
    otp_object = get_valid_otp_object(user = user, purpose='FP', otp = otp)
    if not otp_object:
        raise Http404();
    if request.method == 'GET':
        f = SetPasswordForm()
    else:
        f = SetPasswordForm(request.POST)
        if f.is_valid():
            user.set_password(f.cleaned_data['new_password'])
            user.save()
            otp_object.delete()
            return render(request, 'account/auth/set_password_success.html', { 'u' : user})
    context = { 'f' : f, 'otp': otp_object.otp, 'uid': user.id}
    return render(request, 'account/auth/set_password.html', context)

@require_GET
@login_required
def home(request, id):
    return render(request, 'account/auth/loggedin.html')

def logout(request):
    auth_logout(request)
    return redirect(reverse('login'));

def signup(request):
    if request.user.is_authenticated():
        return redirect(reverse('home', kwargs={'id': request.user.id}));
    if request.method == 'GET':
        context = { 'f' : SignupForm()};
        return render(request, 'account/auth/signup.html', context);
    else:
        f = SignupForm(request.POST,request.FILES);
        if not f.is_valid():
            return render(request, 'account/auth/signup.html', {'f' : f});
        else:
            user = f.save(commit = False)
            user.set_password(f.cleaned_data['password'])
            user.is_active = False
            user.save()
            '''
            Geneerate OTP for activate account
            Send EMAIL
            Show Success Page
            '''
            return HttpResponse('ok');

''' Activate Account '''
@require_GET
def activate(request, id = None, otp = None):
    '''
    Verify id, otp pair
    Fetch User
    set user.is_active = True
    delete otp object
    Show a success page with login link
    '''
    pass

@require_GET
def get_all_users(request):
    users = MyUser.objects.all()

    my_list = serializers.serialize("xml", users)
    return HttpResponse(my_list, content_type="application/xml")
    data = [ { 'first_name ': user.first_name, 'last_name': user.last_name} for user in users]
    return JsonResponse({'data': data})

