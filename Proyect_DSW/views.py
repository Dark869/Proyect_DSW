from django.shortcuts import render

def home_view(request):
    return render(request, 'signatureFile.html')

def gestorLLaves_view(request):
    return render(request, 'gestorLLaves.html')

def verificarFirma_view(request):
    return render(request, 'verificarFirmas.html')