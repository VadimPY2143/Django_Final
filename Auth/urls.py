from django.urls import path
from Auth.views import register, user_login, user_logout, confirm_registration, resend_confirmation_mail

urlpatterns = [
    path('register/', register, name='register'),
    path('confirm_registration/', confirm_registration, name='confirm_registration'),
    path('resend_confirmation_mail/', resend_confirmation_mail, name='resend_confirmation_mail'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout')
]
