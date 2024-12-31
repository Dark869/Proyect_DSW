from django.shortcuts import render, redirect
from .controllers.decorator import login_request

@login_request
def index_view(request):
    return render(request, 'index.html')

@login_request
def home_view(request):
    username = request.session.get('user')
    return render(request, 'signatureFile.html', {'username': username})

@login_request
def gestorLLaves_view(request):
    username = request.session.get('user')
    return render(request, 'gestorLLaves.html', {'username': username})

@login_request
def verificarFirma_view(request):
    username = request.session.get('user')
    return render(request, 'verificarFirmas.html', {'username': username})

@login_request
def logout_view(request):
    request.session.flush()  

    return redirect('/login/')