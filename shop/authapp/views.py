from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from authapp.forms import ShopUserLoginForm, ShopUserCreationForm, ShopUserChangeForm, ShopUserProfileChangeForm
from authapp.models import ShopUser, ShopUserProfile


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
                if not redirect_to:
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
        profile_form = ShopUserProfileChangeForm(request.POST, request.FILES, instance=request.user.shopuserprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            # profile_form.save() убрал, т.к. добавил сигналы
            # return HttpResponseRedirect(request.path_info)  # вернуться откуда пришли
            return HttpResponseRedirect(reverse('main:main'))
    else:
        form = ShopUserChangeForm(instance=request.user)
        profile_form = ShopUserProfileChangeForm(instance=request.user.shopuserprofile)

    context = {
        'page_title': 'редактирование',
        'form': form,
        'profile_form': profile_form,
    }
    return render(request, 'authapp/update.html', context)


def verify(request, email, activation_key):
    user = get_user_model().objects.get(email=email)
    if user.activation_key == activation_key and not user.is_activation_key_expired:
        user.is_active = True
        user.save()
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return render(request, 'authapp/verification.html')


@receiver(post_save, sender=ShopUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ShopUserProfile.objects.create(user=instance)


@receiver(post_save, sender=ShopUser)
def save_user_profile(sender, instance, **kwargs):
    instance.shopuserprofile.save()
