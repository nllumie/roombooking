from django.urls import path
from .views import BookingListView, BookingCreateView, BookingUpdateView, BookingDeleteView

urlpatterns = [
    path('', BookingListView.as_view(), name='booking_list'),
    path('create/', BookingCreateView.as_view(), name='booking_create'),
    path('<int:pk>/update/', BookingUpdateView.as_view(), name='booking_update'),
    path('<int:pk>/delete/', BookingDeleteView.as_view(), name='booking_delete'),
]

