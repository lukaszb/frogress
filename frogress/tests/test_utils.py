from __future__ import unicode_literals, absolute_import
from frogress.tests.compat import unittest
from frogress.utils import gen_range
from frogress.utils import get_first_attr
from frogress.utils import get_terminal_width
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


class TestFirstAttr(unittest.TestCase):

    def test_first(self):
        obj = DummyObject()
        obj.foo = 1
        obj.bar = 2
        self.assertEqual(get_first_attr(obj, ['foo', 'bar']), 1)
        self.assertEqual(get_first_attr(obj, ['bar', 'foo']), 2)

    def test_no_attr(self):
        obj = DummyObject()
        self.assertIsNone(get_first_attr(obj, ['foo', 'bar']))


def raiser(err):
    def inner(*args, **kwargs):
        raise err
    return inner

class TestTerminalWidth(unittest.TestCase):

    @mock.patch('frogress.utils.struct.unpack')
    def test_index_error(self, unpack):
        unpack.side_effect = raiser(IndexError)
        self.assertIsNone(get_terminal_width())

    @mock.patch('frogress.utils.struct.unpack')
    def test_io_error(self, unpack):
        unpack.side_effect = raiser(IOError)
        self.assertIsNone(get_terminal_width())

    @mock.patch('frogress.utils.struct.unpack')
    def test_other_error(self, unpack):
        unpack.side_effect = raiser(ValueError)
        with self.assertRaises(ValueError):
            get_terminal_width()

    @mock.patch('frogress.utils.struct.unpack')
    def test_get_terminal_width(self, unpack):
        unpack.return_value = ['foo', 80]
        self.assertEqual(get_terminal_width(), 80)

