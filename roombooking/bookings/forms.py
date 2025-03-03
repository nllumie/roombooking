from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        room = cleaned_data.get('room')

        if start_time and end_time and room:
            if end_time <= start_time:
                raise forms.ValidationError("End time must be after start time")

            overlapping_bookings = Booking.objects.filter(
                room=room,
                start_time__lt=end_time,
                end_time__gt=start_time
            )

            if self.instance:
                overlapping_bookings = overlapping_bookings.exclude(id=self.instance.id)

            if overlapping_bookings.exists():
                raise forms.ValidationError("Room is already booked for this time period")

        return cleaned_data

