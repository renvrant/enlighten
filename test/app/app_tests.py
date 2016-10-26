from app import app
import unittest


class EnlightenRootTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_root_redirects(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 302)

    def test_home_data(self):
        result = self.app.get('/common/')
        self.assertIn('All transgressions', result.data)
