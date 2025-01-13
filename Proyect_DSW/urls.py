from django.contrib import admin
from django.urls import path

import Proyect_DSW.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view),
    path('login/', views.login),
    path('register/', views.register),
    path('vfirma/', views.verificarFirma_view),
    path('gllaves/', views.gestorLLaves_view),
    path('logout/', views.logout_view),
]
