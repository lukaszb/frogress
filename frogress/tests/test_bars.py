from __future__ import unicode_literals, absolute_import
from collections.abc import Iterable
from frogress.tests.compat import unittest
from frogress.utils import get_list, gen_range
from frogress.widgets import ProgressWidget
from unittest import mock
import datetime
import frogress
import io


class TestBar(unittest.TestCase):

    def setUp(self):
        self.bar = frogress.Bar([])
        self.bar.output = mock.Mock()

    def test_get_timedelta(self):
        self.bar.started = datetime.datetime(2013, 5, 13, 17, 0, 0)
        now = datetime.datetime(2013, 5, 13, 17, 2, 15, 500000)
        delta = self.bar.get_timedelta(now)
        self.assertEqual(delta, 135.5)

    def test_get_timedelta_not_started_yet(self):
        self.bar.step = 12 # should be ignored
        self.bar.started = None
        self.assertIsNone(self.bar.get_timedelta())

    def test_next(self):
        self.bar.iterable = [1, 2, 3, 4, 5]
        next(self.bar)
        self.assertEqual(self.bar.step, 1)

    def test_step(self):
        self.bar.iterable = gen_range(100)
        self.assertEqual(self.bar.step, 0)
        iterator = iter(self.bar)
        next(iterator)
        self.assertEqual(self.bar.step, 1)
        next(iterator)
        next(iterator)
        next(iterator)
        self.assertEqual(self.bar.step, 4)

    def test_step_callback(self):
        self.bar.iterable = gen_range(100)
        self.bar.step_callback = lambda: 11
        self.assertEqual(self.bar.step, 11)
        self.bar.step_callback = lambda: 209
        self.assertEqual(self.bar.step, 209)

    @mock.patch('frogress.bars.get_terminal_width')
    def test_render(self, get_terminal_width):
        get_terminal_width.return_value = None
        self.bar.iterable = [1, 2, 3]
        self.bar.output = mock.Mock()

        widget1 = mock.Mock()
        widget1.render = mock.Mock(return_value='foo')
        widget2 = mock.Mock()
        widget2.render = mock.Mock(return_value='bar')
        self.bar.widgets = [widget1, widget2]

        self.bar.separator = ' # '
        self.assertEqual(self.bar.render(), 'foo # bar')
        widget1.render.assert_called_once_with(self.bar)
        widget2.render.assert_called_once_with(self.bar)

        self.bar.separator = ' | '
        self.bar.widgets = ['Prefix', widget1]
        self.assertEqual(self.bar.render(), 'Prefix | foo')

    @mock.patch('frogress.bars.get_terminal_width')
    def test_progress(self, get_terminal_width):
        get_terminal_width.return_value = None
        self.bar.iterable = gen_range(3)
        self.bar.output = io.StringIO()
        self.bar.treshold = 0
        self.bar.setup_widgets([ProgressWidget])
        next(self.bar)
        next(self.bar)
        next(self.bar)
        with self.assertRaises(StopIteration):
            next(self.bar)
        output = self.bar.output.getvalue()
        self.assertEqual(output, '\r'.join([
            '\rProgress: 1',
            'Progress: 2',
            'Progress: 3',
            'Progress: 3', # show is called on finish too
        ]))

    def test_iter(self):
        self.bar.iterable = [1, 2, 3]
        items = iter(self.bar)
        self.assertEqual(list(items), [1, 2, 3])
        self.assertIsInstance(self.bar.started, datetime.datetime)
        self.assertIsInstance(self.bar.finished, datetime.datetime)

    def test_show(self):
        self.bar.iterable = [1, 2, 3, 4, 5, 6, 7]
        self.bar.render = mock.Mock(return_value='10/10')
        self.bar.show()

        self.bar.output.write.assert_called_once_with('\r10/10')
        self.bar.output.flush.assert_called_once_with()

    # fails randomly
    #def test_show_sets_last_shown_at(self):
        #self.bar.last_shown_at = None
        #self.bar.show()
        #self.assertIsNotNone(self.bar.last_shown_at)
        #now = datetime.datetime.now()
        #delta = datetime.timedelta(microseconds=400)
        #self.assertAlmostEqual(self.bar.last_shown_at, now, delta=delta)

    def test_show_respects_treshold(self):
        self.bar._show = mock.Mock()
        self.bar.treshold = 50
        self.bar.last_shown_at = datetime.datetime(2013, 5, 13, 1, 41, 50)

        self.bar.show(now=datetime.datetime(2013, 5, 13, 1, 41, 50, 40))
        self.assertFalse(self.bar._show.called)

    def test_get_percentage(self):
        self.bar.iterable = get_list(1000)
        self.bar.steps = 1000
        self.bar.step = 51
        self.assertEqual(self.bar.get_percentage(), 5.1)
        self.bar.step = 103
        self.assertEqual(self.bar.get_percentage(), 10.3)
        self.bar.step = 670
        self.assertEqual(self.bar.get_percentage(), 67)
        self.bar.step = 1000
        self.assertEqual(self.bar.get_percentage(), 100)

    def test_get_percentage_if_len_is_not_known(self):
        self.bar.iterable = gen_range(10)
        self.bar.step = 51
        self.assertIsNone(self.bar.get_percentage())

    def test_setup_widgets_if_no_widgets_passed(self):
        self.bar.DEFAULT_WIDGETS = []
        self.bar.steps = 5
        self.bar.setup_widgets(None)
        self.assertEqual(len(self.bar.widgets), 1)
        self.assertIsInstance(self.bar.widgets[0], frogress.PercentageWidget)

    def test_iterable_property(self):
        self.bar._iterable = 'foobar'
        self.assertEqual(self.bar.iterable, 'foobar')

    def test_is_iterable(self):
        self.assertIsInstance(self.bar, Iterable)

