from unittest import mock
import frogress
import unittest


class TestGetVersion(unittest.TestCase):

    @mock.patch.object(frogress, 'VERSION', (1, 2, 3))
    def test_get_version(self):
        self.assertEqual(frogress.get_version(), '1.2.3')

    @mock.patch.object(frogress, 'VERSION', (1, 2, 3, 'dev'))
    def test_get_version_suffix(self):
        self.assertEqual(frogress.get_version(), '1.2.3dev')

    @mock.patch.object(frogress, 'VERSION', (1, 2, 3, 'dev', 'revZXC'))
    def test_get_version_over_4_elements(self):
        self.assertEqual(frogress.get_version(), '1.2.3dev')

