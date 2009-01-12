import hmac
import sha
from time import time

from django.conf import settings
from django.utils.http import cookie_date

# help.yourapp.com/user@gmail.com/1228117891
HASH_FORMAT = "%s/%s/%s"
COOKIE_FORMAT = "tender_%s"
DOMAIN = settings.TENDER_COOKIE_DOMAIN
SECRET = settings.TENDER_SECRET
AGE = settings.TENDER_COOKIE_AGE

def tender_hash(email, expires, tender=DOMAIN, secret=SECRET):
    """Calculates the tender hash."""
    s = HASH_FORMAT % (tender, email, expires)
    sig = hmac.new(secret, digestmod=sha)
    sig.update(s)
    tender_hash = sig.hexdigest()
    return tender_hash
    
def tenderize_response(response, email, extra_cookies=None):
    """Adds tender cookies to `response.`"""
    expires = time() + AGE
    # Tender wants expires in epoch seconds, expires is set with `cookie_date`
    tender_expires = int(expires)
    cookie_expires = cookie_date(expires)
    hashed = tender_hash(email, tender_expires)
    cookies = dict(expires=expires, hash=hashed, email=email)
    # Add extra Tender cookies: http://tinyurl.com/8vwxyw
    if extra_cookies is not None:
        cookies.update(extra_cookies)
    for key, value in cookies.iteritems():
        cookie = COOKIE_FORMAT % key
        response.set_cookie(cookie, value, expires=cookie_expires, domain=DOMAIN)
    # `response.set_cookie()` incorrectly adds questions to the email cookie.
    # To remove the quotes we set the value again.
    response.cookies['tender_email'].coded_value = email    
    return response