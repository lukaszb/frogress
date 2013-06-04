from frogress.tests.compat import unittest
from frogress import humanize


class TestHumanize(unittest.TestCase):

    def test_size(self):
        self.assertEqual(humanize.size(675), '675B')
        self.assertEqual(humanize.size(1024*1.4), '1kB')
        self.assertEqual(humanize.size(1024*1.6), '1kB')
        self.assertEqual(humanize.size(1024*2.9), '2kB')
        self.assertEqual(humanize.size(1024*1024*2.5), '2.5MB')
        self.assertEqual(humanize.size(1024*1024*256), '256.0MB')
        self.assertEqual(humanize.size(1024*1024*1024*2.334), '2.33G')
        self.assertEqual(humanize.size(1024*1024*1024*2.336), '2.34G')
        self.assertEqual(humanize.size(13983134), '13.3MB')

    def test_time(self):
        self.assertEqual(humanize.time(12.3), '12.3s')
        self.assertEqual(humanize.time(12.8), '12.8s')
        self.assertEqual(humanize.time(65.3), '1min5s')
        self.assertEqual(humanize.time(60*60 + 60*16 + 3), '1h16min3s')
        self.assertEqual(humanize.time(60*60*13 + 2), '13h0min2s')
        self.assertEqual(humanize.time(60*60*25 + 60*51 + 52), '1d1h51min52s')

