from __future__ import unicode_literals, absolute_import
from frogress.tests.compat import unittest
from frogress.utils import gen_range
import frogress
import mock
import tempfile


class TestGetIterableSize(unittest.TestCase):

    def test_list(self):
        self.assertEqual(frogress.get_iterable_size([1, 2, 3]), 3)

    def test_generator(self):
        self.assertEqual(frogress.get_iterable_size(gen_range(3)), None)


class DummyObject(object):
    pass


class TestGetFileInfo(unittest.TestCase):

    def test_file_info_for_non_files(self):
        self.assertIsNone(frogress.get_file_info([]))

    @mock.patch('frogress.utils.os.path.getsize')
    def test_file_info(self, getsize):
        getsize.return_value = 123

        # DummyObject is used here as Mock would always answer True for hasattr
        f = DummyObject()
        f.name = '/foobar.gz'
        f.tell = 'step-callback'
        f.seek = ''
        f.fileno = 1

        self.assertEqual(frogress.get_file_info(f), {
            'filename': '/foobar.gz',
            'size': 123,
            'step_callback': 'step-callback',
        })

    def test_file_info_for_temp_file(self):
        with tempfile.NamedTemporaryFile('w') as tmp:
            tmp.write('foobar')
            tmp.flush()
            f = open(tmp.name)
            self.assertEqual(frogress.get_file_info(f), {
                'filename': tmp.name,
                'size': 6,
                'step_callback': f.tell,
            })

