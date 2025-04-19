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
        form = forms.CustomUserCreationForm(request.POST)
        users = CreateUser.objects.all()
        if form.is_valid() and form.cleaned_data['email'] not in [user.email for user in users]:
            rand_code = ''.join(str(randint(0, 9)) for _ in range(4))

            send_mail_task.delay(
                'Code Confirmation',
                f'Your code: {rand_code}',
                'vadimpapusha2310@gmail.com',
                [request.user.email],
            )

            request.session['random_code'] = rand_code
            request.session['form_data'] = {
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'phone_number': form.cleaned_data['phone_number'],
                'password': form.cleaned_data['password'],
                'confirm_password': form.cleaned_data['confirm_password'],
            }
            return render(request, 'verification_page.html', {'form_data': request.session['form_data']})

    else:
        form = forms.CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def confirm_registration(request):
    if request.method == 'POST':
        form_data = request.session.get('form_data', {})
        user_code = request.POST.get('code').strip()
        random_code = request.session.get('random_code')

        if form_data and str(random_code) == user_code:
            query_dict = QueryDict('', mutable=True)
            query_dict.update({
                'username': form_data.get('username'),
                'email': form_data.get('email'),
                'phone_number': form_data.get('phone_number'),
                'password': form_data.get('password'),
                'confirm_password': form_data.get('confirm_password'),
            })
            form = forms.CustomUserCreationForm(query_dict)

            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('main')

            else:
                print('Form validation failed:', form.errors)
        else:
            print('wrong user code')

    return render(request, 'verification_page.html')


def resend_confirmation_mail(request):
    random_code = request.session.get('random_code')
    send_mail_task.delay(
        'Code Confirmation',
        f'Your code: {random_code}',
        'vadimpapusha2310@gmail.com',
        [request.user.email],
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



