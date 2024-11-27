from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView,  RedirectView
from .views import *

router = DefaultRouter()


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]