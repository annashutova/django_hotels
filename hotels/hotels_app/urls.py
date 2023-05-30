from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'amenity', views.AmenityViewSet, basename='amenity')
router.register(r'hotel', views.HotelViewSet, basename='hotel')
router.register(r'room', views.RoomViewSet, basename='room')

urlpatterns = [
    # REST
    path('rest/', include(router.urls)),
    # main urls
    path('', views.main_page, name='main page'),
    path('find/', views.find_page, name='find')
]
