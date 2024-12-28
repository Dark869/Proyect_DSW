from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render, redirect
import Proyect_DSW.settings as config

# Create your views here.

def login(request):
    t = 'login.html'
    if request.method == 'GET':
        return render(request, t)
    
def register(request):
    t = 'register.html'
    if request.method == 'GET':
        return render(request, t)