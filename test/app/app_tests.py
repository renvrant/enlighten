from ..base.base_test_case import BaseTestCase


class EnlightenRootTests(BaseTestCase):

    def test_root_redirects(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 302)

    def test_home_data(self):
        result = self.app.get('/common/')
        self.assertIn('All Incidents', result.data)
