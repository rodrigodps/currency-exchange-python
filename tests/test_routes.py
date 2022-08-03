import os
from unittest import TestCase

from routes import app


class TestRoutes(TestCase):

    @classmethod
    def setUpClass(cls):
        os.environ['DATABASE_DIR'] = '../db/'

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_convert(self):
        '''
        Test currency converter
        '''
        result = self.app.get('/convert?user_id=test&source=BRL&target=USD&amount=10.0')
        self.assertEqual(200, result.status_code)
        currency = result.json['currency']
        source_amount = result.json['source_amount']
        target_amount = result.json['target_amount']
        self.assertEqual(target_amount, source_amount * currency)

    def test_bad_request_convert(self):
        '''
        Test currency converter
        '''
        result = self.app.get('/convert')
        self.assertEqual(400, result.status_code)
        details = result.json['details']
        self.assertEqual(4, len(details))
        self.assertIn('user_id is required', details)
        self.assertIn('amount is required', details)
        self.assertIn('source is required', details)
        self.assertIn('target is required', details)

    def test_bad_request_empty_convert(self):
        '''
        Test currency converter
        '''
        result = self.app.get('/convert?user_id=&source=&target=&amount=')
        self.assertEqual(400, result.status_code)
        details = result.json['details']
        self.assertEqual(4, len(details))
        self.assertIn('user_id is required', details)
        self.assertIn('amount is required', details)
        self.assertIn('source is required', details)
        self.assertIn('target is required', details)

    def test_bad_request_invalid_amount_convert(self):
        '''
        Test currency converter
        '''
        result = self.app.get('/convert?user_id=test&source=BRL&target=USD&amount=R$10.0')
        self.assertEqual(400, result.status_code)
        details = result.json['details']
        self.assertEqual(1, len(details))
        self.assertIn('amount: Value R$10.0 is invalid', details)

    def test_bad_request_invalid_source_convert(self):
        '''
        Test currency converter
        '''
        result = self.app.get('/convert?user_id=test&source=BRA&target=USD&amount=10.0')
        self.assertEqual(400, result.status_code)
        details = result.json['details']
        self.assertEqual(1, len(details))
        self.assertIn('source: Value BRA is invalid. Valid values: [\'EUA\', \'USD\', \'BRL\', \'JPY\']', details)

    def test_bad_request_invalid_target_convert(self):
        '''
        Test currency converter
        '''
        result = self.app.get('/convert?user_id=test&source=BRL&target=USA&amount=10.0')
        self.assertEqual(400, result.status_code)
        details = result.json['details']
        self.assertEqual(1, len(details))
        self.assertIn('target: Value USA is invalid. Valid values: [\'EUA\', \'USD\', \'BRL\', \'JPY\']', details)
