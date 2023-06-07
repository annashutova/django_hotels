from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hotels_app.urls')),
]

admin.site.site_header = 'Hotels Admin Panel'
