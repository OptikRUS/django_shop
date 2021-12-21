from django.shortcuts import render
from authapp.forms import ShopUserLoginForm
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse


def login(request):
    if request.method == 'POST':
        form = ShopUserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)  # cookie creation
                # return HttpResponseRedirect('/')
                return HttpResponseRedirect(reverse('main:main'))
    else:
        form = ShopUserLoginForm()
    context = {
        'page_title': 'логин',
        'form': form,
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:main'))
