from django.contrib import admin
from django.urls import path
import Proyect_DSW.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view),
]
