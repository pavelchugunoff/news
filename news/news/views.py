from django.shortcuts import redirect, render

from authentication.views import redirectWithCookies


def index(request):
    """
    If there is a token, it redirects to a page with messages, and if not, it asks you to log in
    """
    if request.COOKIES.get("token") == None:
        return render(request, 'auth/welcome.html')
    else:
        return redirectWithCookies('http://0.0.0.0:8000/posts', 'token', request.COOKIES.get('token'))
    