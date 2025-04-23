from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from paypal.standard.forms import PayPalPaymentsForm
import uuid
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from Object.models import CreateObject
from .forms import BookForm, EditBookingForm
from .models import Booking
from .tasks import send_html_mail
from django.contrib.auth.decorators import login_required
from Django.settings import PAYPAL_RECEIVER_EMAIL


def book_and_pay(request, object_id):
    objectt = get_object_or_404(CreateObject, id=object_id)

    if request.user.is_authenticated:
        initial_data = {
            'name': request.user.username,
            'surname': request.user.last_name,
            'email': request.user.email,
            'phone': getattr(request.user, 'phone_number', '')
        }
    else:
        initial_data = {}

    if request.method == 'POST':
        post_data = request.POST.copy()
        for key, value in initial_data.items():
            if not post_data.get(key):
                post_data[key] = value

        form = BookForm(post_data)
        dates = Booking.objects.filter(object=objectt).values_list('date_from', 'date_to')

        if form.is_valid():
            new_date_from = form.cleaned_data['date_from']
            new_date_to = form.cleaned_data['date_to']
            for date_from, date_to in dates:
                if date_from <= new_date_from <= date_to:
                    form.add_error('date_from', 'This date is already booked')
                elif date_from <= new_date_to <= date_to:
                    form.add_error('date_to', 'This date is already booked')

            if form.errors:
                return render(request, 'book.html', {'form': form, 'object': objectt})

            booking = form.save(commit=False)
            booking.object = objectt
            booking.user = request.user if request.user.is_authenticated else None
            booking.save()
            booking_days = (booking.date_to - booking.date_from).days + 1
            host = request.get_host()
            paypal_dict = {
                "business": PAYPAL_RECEIVER_EMAIL,
                "amount": objectt.price * booking_days,
                "item_name": objectt.name,
                "invoice": str(uuid.uuid4()),
                "currency_code": "USD",
                'notify_url': f"http://{host}{reverse('paypal-ipn')}",
                'return_url': f"http://{host}{reverse('payment-success', kwargs={'booking_id': booking.id})}",
                'cancel_url': f"http://{host}{reverse('payment-failed', kwargs={'booking_id': booking.id})}",
            }

            paypal_payment = PayPalPaymentsForm(initial=paypal_dict)

            return render(request, 'payment.html', {'paypal': paypal_payment, 'booking_id': booking.id})

    else:
        form = BookForm(initial=initial_data)

    return render(request, 'book.html', {'form': form, 'object': objectt})


@never_cache
def booking_list(request, user_id):
    bookings = Booking.objects.filter(user=user_id)
    return render(request, 'booking_history.html', {'bookings': bookings})


@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    return redirect('booking_list', user_id=request.user.id)


@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    objectt = get_object_or_404(CreateObject, id=booking.object.id)
    booking_days = (booking.date_to - booking.date_from).days + 1
    if request.method == 'POST':
        form = EditBookingForm(request.POST, instance=booking)
        if form.is_valid():
            new_days = (form.cleaned_data['date_to'] - form.cleaned_data['date_from']).days + 1
            if booking_days != new_days:
                form.add_error('date_to', 'The number of days can not be changed')
            else:
                form.save()
                return redirect('booking_list', user_id=request.user.id)
    else:
        form = EditBookingForm(instance=booking)

    return render(request, 'edit_booking.html', {'form': form, 'booking': booking, 'object': objectt})


def payment_done(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    objectt = get_object_or_404(CreateObject, id=booking.object.id)
    html_message = render_to_string('email_message.html', {'booking': booking, 'objectt': objectt})
    plain_message = strip_tags(html_message)
    send_html_mail.delay(plain_message, html_message, booking.email)
    booking.paid = True
    booking.save()
    return render(request, 'payment_done.html', {"object": objectt})


def payment_canceled(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    objectt = get_object_or_404(CreateObject, id=booking.object.id)
    return render(request, 'payment_canceled.html', {"object": objectt})



