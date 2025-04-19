from django.urls import path
from .views import book_and_pay, booking_list, edit_booking, payment_done, payment_canceled, delete_booking

urlpatterns = [
    path('<int:object_id>/', book_and_pay, name='book'),
    path('booking_list/<int:user_id>/', booking_list, name='booking_list'),
    path('booking_edit/<int:booking_id>/', edit_booking, name='booking_edit'),
    path('delete_booking/<int:booking_id>/', delete_booking, name='delete_booking'),
    path('payment_done/<int:booking_id>/', payment_done, name='payment-success'),
    path('payment_canceled/<int:booking_id>/', payment_canceled, name='payment-failed'),
]
