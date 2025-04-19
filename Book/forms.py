from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError

from .models import Booking


class BookForm(forms.ModelForm):
    date_from = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    date_to = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Booking
        fields = ['name', 'surname', 'phone', 'email', 'human_count', 'date_from', 'date_to']

    def clean(self):

        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')

        if date_from and date_to and date_to <= date_from:
            raise ValidationError({'date_to': 'Date from can not be earlier than date to.'})

        elif date_from and date_to < datetime.now().date():
            raise ValidationError({'date_from': 'Date from can not be earlier than today.'})

        return cleaned_data


class EditBookingForm(forms.ModelForm):
    date_from = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    date_to = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Booking
        fields = ['date_from', 'date_to']