from django.contrib import admin
from django.urls import path

import db.views as dbVistas
import Proyect_DSW.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view),
    path('login/', dbVistas.login),
    path('register/', dbVistas.register),
    path('vFirma/', dbVistas.verificarFirma),
]
