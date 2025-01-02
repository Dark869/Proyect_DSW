from django.shortcuts import render, redirect
from .controllers.decorator import login_request
from .controllers.signFile import sing_file

@login_request
def index_view(request):
    return render(request, 'index.html')

@login_request
def home_view(request):
    username = request.session.get('user')

    if request.method == 'GET':
        return render(request, 'signatureFile.html', {'username': username})
    else:
        file = request.POST.get('file')
        passwd = request.POST.get('passwd')
        sing_file(passwd, file, username)
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