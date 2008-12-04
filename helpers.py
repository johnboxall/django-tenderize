import hmac
import sha
from time import time

from django.conf import settings

# http://help.tenderapp.com/faqs/setup-installation/login-from-cookies
FORMAT = "%s/%s/%s"

def tender_hash(email, expires=None, tender=settings.TENDER_DOMAIN, secret=settings.TENDER_SECRET):
    if expires is None:
        expires = int(time()) + (60 * 60 * 72) # 72 hours
    s = FORMAT % (tender, email, expires)
        
    sig = hmac.new(secret, digestmod=sha)    
    sig.update(s)
    tender_hash = sig.hexdigest()
    return tender_hash