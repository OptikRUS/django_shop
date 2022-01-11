from django.shortcuts import render
from authapp.forms import ShopUserLoginForm, ShopUserCreationForm, ShopUserChangeForm
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model


def login(request):
    redirect_to = request.GET.get('next', '')
    if request.method == 'POST':
        form = ShopUserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            redirect_to = request.POST.get('redirect-to')
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)  # cookie creation
                if redirect_to:
                    return HttpResponseRedirect(redirect_to or reverse('main:main'))
    else:
        form = ShopUserLoginForm()
    content = {
        'page_title': 'логин',
        'form': form,
        'redirect_to': redirect_to,
    }
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:main'))


def register(request):
    if request.method == 'POST':
        form = ShopUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_activation_key()
            user.save()
            if not user.send_confirm_email():
                return HttpResponseRedirect(reverse('auth:register'))
            return HttpResponseRedirect(reverse('main:main'))
    else:
        form = ShopUserCreationForm()

    context = {
        'page_title': 'регистрация',
        'form': form,
    }
    return render(request, 'authapp/register.html', context)


def edit(request):
    if request.method == 'POST':
        form = ShopUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            # return HttpResponseRedirect(request.path_info)  # вернуться откуда пришли
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        form = ShopUserChangeForm(instance=request.user)

    context = {
        'page_title': 'редактирование',
        'form': form,
    }
    return render(request, 'authapp/update.html', context)


def verify(request, email, activation_key):
    user = get_user_model().objects.get(email=email)
    if user.activation_key == activation_key and not user.is_activation_key_expired:
        user.is_active = True
        user.save()
        auth.login(request, user)
    return render(request, 'authapp/verification.html')
