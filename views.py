from time import time

from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from tenderize.helpers import tender_hash

@login_required
def tenderize(request):
    """Example of logging a user into tender."""
    email = request.user.email
    expires = int(time()) + (60 * 60 * 72) # 72 hours
    hashed = tender_hash(email, expires)

    response = HttpResponse('Tenderizing %s/%s/%s' % (email, expires, hashed))
    response.set_cookie('tender_email', email, domain=settings.TENDER_COOKIE_DOMAIN)
    response.set_cookie('tender_expires', expires, domain=settings.TENDER_COOKIE_DOMAIN)
    response.set_cookie('tender_hash', hashed, domain=settings.TENDER_COOKIE_DOMAIN)
    return response

