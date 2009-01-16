import unittest

from django.test.client import Client
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from tenderize.helpers import tender_hash, tenderize_response
from tenderize.views import login_and_tenderize


class TenderizeTestCase(unittest.TestCase):
    def setUp(self):
        self.user = 'user'
        self.email = 'user@gmail.com'
        self.password = 'password'
        self.tender = 'help.yourapp.com'
        self.expires = 1228117891
        self.secret = 'monkey'

    def testTenderHash(self):
        result = tender_hash(self.email, self.expires, self.tender, self.secret)
        self.assertEquals(result, '1937bf7e8dc9f475cc9490933eb36e5f7807398a')

    def testTenderizeResponse(self):
        # Tenderized response will contain Tender cookies.
        response = HttpResponse('Test Response')
        response = tenderize_response(response, self.email, {'user': self.user})
        self.assertEqual(response.cookies['tender_email'].value, self.email)
        self.assertEqual(response.cookies['tender_user'].value, self.user)
        self.assertTrue('tender_expires' in response.cookies)
        self.assertTrue('tender_hash' in response.cookies)
                
    def testLoginAndTenderize(self):
        c = Client()
        user = User.objects.create_user(self.user, self.email, self.password)
        # Correct login returns HttpResponseRedirect
        login = reverse('login')
        response = c.post(login, {'username': self.user, 'password': self.password})
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertTrue('tender_expires' in response.cookies)
        self.assertTrue('tender_hash' in response.cookies)
        self.assertTrue('tender_email' in response.cookies)
        # Bad login returns HttpResponse
        response = c.post(login, {'username': self.user, 'password': 'EVIL'})
        self.assertTrue(isinstance(response, HttpResponse))