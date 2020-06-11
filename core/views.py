from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import Permission, User


def index(request):
    """ Index page """
    context = {}
    return render(request, 'core/index.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            view_perm = Permission.objects.get(codename="view_ingredient")
            create_perm = Permission.objects.get(codename="add_ingredient")
            change_perm = Permission.objects.get(codename="change_ingredient")
            user.user_permissions.add(view_perm)
            user.user_permissions.add(create_perm)
            user.user_permissions.add(change_perm)
            login(request, user)
            return redirect(reverse_lazy('core:index'))
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(
            request.POST, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse_lazy('core:index'))
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('core:index'))
