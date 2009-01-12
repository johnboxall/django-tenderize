import unittest

from django.http import HttpResponse

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
        response = HttpResponse('Test Response')
        response = tenderize_response(response, self.email, {'user': self.user})
        self.assertEqual(response.cookies['tender_email'].value, self.email)
        self.assertEqual(response.cookies['tender_user'].value, self.user)
        self.assertTrue('tender_expires' in response.cookies)
        self.assertTrue('tender_hash' in response.cookies)