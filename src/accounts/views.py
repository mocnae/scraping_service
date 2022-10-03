from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect

from accounts.forms import UserLoginForm, UserRegistrationForm, UpdateUserForm
User = get_user_model()


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('scraping:home_authorized')
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('scraping:home')


def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password1'])
        new_user.save()
        return render(request, 'register_done.html', {'new_user': new_user})
    return render(request, 'register.html', {'form': form})


def update_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UpdateUserForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.city = data['city']
                user.language = data['language']
                user.send_email = data['send_email']
                user.save()
                return redirect('accounts:update')
        else:
            form = UpdateUserForm(initial={'city': user.city, 'language': user.language,
                                           'send_email': user.send_email})
        return render(request, 'update.html', {'form': form})
    else:
        return redirect('accounts:login')


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)
            qs.delete()
    return redirect('home')
