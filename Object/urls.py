from django.urls import path
from Object.views import create_object, main, about, contact, search_objects, user_profile

urlpatterns = [
    path('create/', create_object, name='create'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('search_objects/', search_objects, name='search_objects'),
    path('user_profile/', user_profile, name='user_profile'),
    path('', main, name='main')
]
