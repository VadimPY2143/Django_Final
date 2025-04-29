from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import QueryDict
import Auth.forms as forms
from Auth.models import CreateUser
from random import randint
from .tasks import send_mail_task


def register(request):
    if request.method == 'POST':
        form = forms.CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            rand_code = ''.join(str(randint(0, 9)) for _ in range(4))
            send_mail_task.delay(
                'Code Confirmation',
                f'Your code: {rand_code}',
                'vadimpapusha2310@gmail.com',
                [form.cleaned_data['email']],
            )

            request.session['random_code'] = rand_code
            request.session['user_id'] = user.id

            return render(request, 'verification_page.html')

    else:
        form = forms.CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


def confirm_registration(request):
    if request.method == 'POST':
        user_code = request.POST.get('code', '').strip()
        random_code = request.session.get('random_code')
        user_id = request.session.get('user_id')

        if user_code == str(random_code):
            user = CreateUser.objects.get(id=user_id)
            user.is_active = True
            user.save()

            del request.session['random_code']
            del request.session['user_id']

            login(request, user)
            return redirect('main')

        return render(request, 'verification_page.html')

    return render(request, 'verification_page.html')


def resend_confirmation_mail(request):
    random_code = request.session.get('random_code')
    user_id = request.session.get('user_id')
    user = CreateUser.objects.get(id=user_id)
    send_mail_task.delay(
        'Code Confirmation',
        f'Your code: {random_code}',
        'vadimpapusha2310@gmail.com',
        [user.email],
        )
    return render(request, 'verification_page.html')


def user_login(request):
    if request.method == 'POST':
        form = forms.CustomAuthenticationForm(request.POST)

        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            form.add_error(None, 'Будь ласка, введіть ім’я користувача та пароль.')

        else:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                ...

    else:
        form = forms.CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You are logged out')
    return redirect('main')



