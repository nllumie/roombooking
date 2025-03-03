from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.core.mail import send_mail
from .models import Booking
from .forms import BookingForm


class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('booking_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        self.send_booking_confirmation(self.object)
        return response

    def send_booking_confirmation(self, booking):
        subject = f'Room Booking Confirmation: {booking.room.name}'
        message = f'''
        Dear {booking.user.username},

        Your booking for {booking.room.name} has been confirmed.

        Date and Time: {booking.start_time.strftime('%Y-%m-%d %H:%M')} to {booking.end_time.strftime('%H:%M')}
        Location: {booking.room.location}

        Thank you for using our Room Booking System.
        '''

        send_mail(subject, message, 'noreply@company.com', [booking.user.email])


class BookingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('booking_list')

    def test_func(self):
        booking = self.get_object()
        return self.request.user == booking.user or self.request.user.is_staff

    def form_valid(self, form):
        response = super().form_valid(form)
        self.send_booking_update_notification(self.object)
        return response

    def send_booking_update_notification(self, booking):
        subject = f'Room Booking Updated: {booking.room.name}'
        message = f'''
        Dear {booking.user.username},

        Your booking for {booking.room.name} has been updated.

        New Date and Time: {booking.start_time.strftime('%Y-%m-%d %H:%M')} to {booking.end_time.strftime('%H:%M')}
        Location: {booking.room.location}

        Thank you for using our Room Booking System.
        '''

        send_mail(subject, message, 'noreply@company.com', [booking.user.email])


class BookingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Booking
    success_url = reverse_lazy('booking_list')
    template_name = 'bookings/booking_confirm_delete.html'

    def test_func(self):
        booking = self.get_object()
        return self.request.user == booking.user or self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        booking = self.get_object()
        response = super().delete(request, *args, **kwargs)
        self.send_booking_cancellation(booking)
        return response

    def send_booking_cancellation(self, booking):
        subject = f'Room Booking Cancelled: {booking.room.name}'
        message = f'''
        Dear {booking.user.username},

        Your booking for {booking.room.name} has been cancelled.

        Date and Time: {booking.start_time.strftime('%Y-%m-%d %H:%M')} to {booking.end_time.strftime('%H:%M')}

        Thank you for using our Room Booking System.
        '''

        send_mail(subject, message, 'noreply@company.com', [booking.user.email])

