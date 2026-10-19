from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
def register(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request,'Passwords do not match')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request,'Username already exists')
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
            )

        user.save()
        messages.success(
            request,
            'Registration successful. Please login.')
        return redirect('login')

    return render(
        request,
        'accounts/register.html'
        )
def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                'Login successful.'
            )

            return redirect('home')

        else:

            messages.error(
                request,
                'Invalid username or password.'
            )

            return redirect('login')

    return render(
        request,
        'accounts/login.html'
    )


def user_logout(request):

    logout(request)

    messages.success(
        request,
        'You have been logged out.'
    )

    return redirect('home')

@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Your profile has been updated successfully!'
            )
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(
        request,
        'accounts/profile.html',
        {'form': form}
    )

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(
            user=request.user,
            data=request.POST
        )

        if form.is_valid():
            user = form.save()

            update_session_auth_hash(request, user)

            messages.success(
                request,
                'Your password has been changed successfully!'
            )
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(
        request,
        'accounts/change_password.html',
        {'form': form}
    )
