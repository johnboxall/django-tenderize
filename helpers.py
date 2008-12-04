import hmac
import sha
from time import mktime
from datetime import datetime, timedelta

from django.conf import settings

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
    expires = datetime.now() + timedelta(seconds=settings.TENDER_COOKIE_AGE)
    tender_expires = int(mktime(expires.timetuple())) # Tender wants expires in epoch
    cookie_expires = expires.strftime("%a, %d-%b-%Y %H:%M:%S UTC") # Set cookie wants expires in UTC    
    hashed = tender_hash(email, tender_expires)
    response.set_cookie('tender_email', email, expires=cookie_expires, domain=settings.TENDER_COOKIE_DOMAIN)
    response.set_cookie('tender_expires', tender_expires, expires=cookie_expires, domain=settings.TENDER_COOKIE_DOMAIN)
    response.set_cookie('tender_hash', hashed, expires=cookie_expires, domain=settings.TENDER_COOKIE_DOMAIN)
    return response