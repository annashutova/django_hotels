from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'amenity', views.AmenityViewSet, basename='amenity')
router.register(r'hotel', views.HotelViewSet, basename='hotel')
router.register(r'room', views.RoomViewSet, basename='room')
router.register(r'booking', views.BookingViewSet, basename='booking')

urlpatterns = [
    # REST
    path('rest/', include(router.urls)),
    # main urls
    path('', views.main_page, name='main page'),
    path('find/', views.find_page, name='find'),
    path('account/', views.account, name='account page'),
    path('rooms/', views.rooms_page, name='rooms page'),
    path('register/', views.register, name='register'),
    path('log_in/', views.login_view, name='log in'),
    path('log_out/', views.logout_view, name='log out'),
    path('book/', views.booking_page, name='book'),
    path('bookings/current/', views.current_bookings, name='current bookings'),
    path('bookings/past/', views.past_bookings, name='past bookings'),
    path('confirmation/', views.booking_confirmation, name='confirm booking'),
    path('fail/', views.failed_booking, name='fail'),
    path('success/', views.successful_booking, name='success'),
]
