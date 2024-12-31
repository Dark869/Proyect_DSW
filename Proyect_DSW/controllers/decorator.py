from django.shortcuts import redirect

SESSION_LOGGED_KEY = 'logged'

def login_request(view):
    def interna(request, *args, **kargs):
        if not request.session.get(SESSION_LOGGED_KEY, False):
            return redirect('/login')
        return view(request, *args, **kargs)
    return interna