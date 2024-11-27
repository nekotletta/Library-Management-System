from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView,  RedirectView
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'reservations', ReservationsViewSet)
router.register(r'waitlist', WaitlistViewSet)

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
