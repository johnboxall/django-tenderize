import unittest

from django_tenderize.helpers import tender_hash

class TenderHashTestCase(unittest.TestCase):
    def testTenderHash(self):
        email = 'user@gmail.com'
        tender = 'help.yourapp.com'
        expires = 1228117891
        secret = 'monkey'
        self.assertEquals(tender_hash(email, expires, tender, secret), '1937bf7e8dc9f475cc9490933eb36e5f7807398a')