from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page, never_cache
from django.core.cache import cache
from Book.models import Booking
from Object.forms import CreateObjForm
from Object.models import CreateObject


def create_object(request):
    if request.method == 'POST':
        form = CreateObjForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main')
    else:
        form = CreateObjForm()
    return render(request, 'create_obj.html', {'form': form})


def main(request):
    objectt = CreateObject.objects.all()
    if not request.user.is_authenticated:
        responsee = cache_page(60 * 15)(render)(request, 'main.html', {'object': objectt})

    else:
        responsee = render(request, 'main.html', {'object': objectt})

    return responsee


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def search_objects(request):
    query = request.GET.get('q')
    objects = CreateObject.objects.filter(name__contains=query)
    return render(request, 'search_objects.html', {'objects': objects if len(objects) != 0 else 'No objects found',
                                                   'query': query})


@never_cache
def user_profile(request):
    user = request.user
    bookings = len(Booking.objects.filter(user=user))
    return render(request, 'user_profile.html', {'user': user, 'bookings': bookings})
