import serializers
from .models import Booking
from rooms.serializers import RoomSerializer
from users.serializers import UserSerializer
from django.utils import timezone
from datetime import timedelta


class BookingSerializer(serializers.ModelSerializer):
    room_details = RoomSerializer(source='room', read_only=True)
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Booking
        fields = ('id', 'room', 'user', 'start_time', 'end_time', 'status',
                  'created_at', 'updated_at', 'room_details', 'user_details')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at', 'room_details', 'user_details')

    def validate(self, data):
        # Check if end_time is after start_time
        if data['end_time'] <= data['start_time']:
            raise serializers.ValidationError("End time must be after start time")

        # Check if start_time is in the future
        if data['start_time'] < timezone.now():
            raise serializers.ValidationError("Cannot book room in the past")

        # Check for overlapping bookings
        room = data['room']
        start_time = data['start_time']
        end_time = data['end_time']

        overlapping_bookings = Booking.objects.filter(
            room=room,
            status='confirmed',
            start_time__lt=end_time,
            end_time__gt=start_time
        )

        # Exclude current booking when updating
        if self.instance:
            overlapping_bookings = overlapping_bookings.exclude(id=self.instance.id)

        if overlapping_bookings.exists():
            raise serializers.ValidationError("Room is already booked for this time period")

        return data

    def create(self, validated_data):
        # Set user to current user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

