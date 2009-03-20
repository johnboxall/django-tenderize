from django.http import HttpResponseRedirect
from django.contrib.auth.views import login, logout, logout_then_login
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.cache import never_cache

from tenderize.helpers import tenderize_response, detenderize_response


def login_and_tenderize(request, template_name='registration/login.html', 
                        redirect_field_name=REDIRECT_FIELD_NAME, extra_cookies=None):
    """
    Displays the login form and handles the login action. Sets Tender cookies if successful.
    
    """
    response = login(request, template_name, redirect_field_name)    
    # login returns a HttpResponseRedirect if successful.
    if isinstance(response, HttpResponseRedirect):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            tenderize_response(response, user.email, extra_cookies)
    return response
login_and_tenderize = never_cache(login_and_tenderize)

def logout_and_detenderize(request, next_page=None, template_name='registration/logged_out.html'):
    """
    Logs out the user and removes Tender cookies.
    
    """
    response = logout(request, next_page, template_name)
    detenderize_response(response)
    return response

def logout_detenderize_and_login(request, login_url=None):
    """
    Logs the user out and removes Tender cookies. Redirects to log-in page.
    
    """
    response = logout_then_login(request, login_url)
    detenderize_response(response)
    return response