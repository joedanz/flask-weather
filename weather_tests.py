import os
import weather
import datetime
import unittest
import tempfile

class WeatherTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, weather.app.config['DATABASE'] = tempfile.mkstemp()
        weather.app.config['TESTING'] = True
        self.app = weather.app.test_client()
        weather.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(weather.app.config['DATABASE'])

    def test_empty_db(self):
        """Test empty database with no entries."""
        rv = self.app.get('/')
        assert 'Nothing logged yet.' in rv.data

    def test_report(self):
        """Test reporting weather"""
        rv = self.app.get('/report/11210/63/23', follow_redirects=True)
        assert b'11210' in rv.data

    def test_full_db(self):
        """Test reporting weather"""
        rv = self.app.get('/', follow_redirects=True)
        assert b'11210' in rv.data

if __name__ == '__main__':
    unittest.main()
