import hmac
import sha
from time import time

from django.conf import settings
from django.utils.http import cookie_date

# help.yourapp.com/user@gmail.com/1228117891
FORMAT = "%s/%s/%s"

def tender_hash(email, expires, tender=settings.TENDER_DOMAIN, secret=settings.TENDER_SECRET):
    """Calculates the tender hash."""
    s = FORMAT % (tender, email, expires)
    sig = hmac.new(secret, digestmod=sha)
    sig.update(s)
    tender_hash = sig.hexdigest()
    return tender_hash
    
def tenderize_response(response, email):
    """Adds tender cookies to the response"""
    expires = time() + settings.TENDER_COOKIE_AGE
    tender_expires = int(expires)  # Tender wants expires in epoch seconds
    cookie_expires = cookie_date(expires)  # Cookie time for the cookie
    hashed = tender_hash(email, tender_expires)
    response.set_cookie('tender_expires', tender_expires, expires=cookie_expires, domain=settings.TENDER_COOKIE_DOMAIN)
    response.set_cookie('tender_hash', hashed, expires=cookie_expires, domain=settings.TENDER_COOKIE_DOMAIN)
    response.set_cookie('tender_email', email, expires=cookie_expires, domain=settings.TENDER_COOKIE_DOMAIN)
    # response.set_cookie() incorrectly sets coded_value to "<email>"
    # we need to override that default value be just <email>
    response.cookies['tender_email'].coded_value = email    
    return response