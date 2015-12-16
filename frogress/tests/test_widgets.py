from __future__ import unicode_literals, absolute_import
from frogress.tests.compat import unittest
from frogress.utils import gen_range
import frogress
import io
import mock


class TestBaseWidget(unittest.TestCase):
    widget_class = None
    widget_attrs = {}

    def setUp(self):
        self.bar = mock.Mock()
        self.widget = self.widget_class()
        for key, value in self.widget_attrs.items():
            setattr(self.widget, key, value)


    def assertRenderedWidgetEqual(self, expected):
        self.assertEqual(self.widget.render(self.bar), expected)


class TestWidget(TestBaseWidget):
    widget_class = frogress.Widget

    def test_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.widget.render(self.bar)

class TestProgressWidget(TestBaseWidget):
    widget_class = frogress.ProgressWidget

    def test_render(self):
        self.bar.step = 102
        self.bar.steps = None
        self.assertRenderedWidgetEqual('Progress: 102')

    def test_render_known_steps(self):
        self.bar.step = 102
        self.bar.steps = 150
        self.assertRenderedWidgetEqual('Progress: 102 / 150')

    def test_render_prefix_changed(self):
        self.widget.prefix = 'Steps: '
        self.bar.step = 102
        self.bar.steps = None
        self.assertRenderedWidgetEqual('Steps: 102')


class TestPercentageWidget(TestBaseWidget):
    widget_class = frogress.PercentageWidget

    def test_render(self):
        self.bar.get_percentage = mock.Mock(return_value=6.2)
        self.assertRenderedWidgetEqual('  6.2%')
        self.bar.get_percentage = mock.Mock(return_value=56.0)
        self.assertRenderedWidgetEqual(' 56.0%')
        self.bar.get_percentage = mock.Mock(return_value=100.0)
        self.assertRenderedWidgetEqual('100.0%')


class TestTransferWidget(TestBaseWidget):
    widget_class = frogress.TransferWidget
    widget_attrs = {'prefix': ''}

    def test_render_without_steps(self):
        self.bar.step = 1024 * 45
        self.bar.steps = 0
        self.assertRenderedWidgetEqual('45kB')

    def test_render(self):
        self.bar.step = 101
        self.bar.steps = 1024
        self.assertRenderedWidgetEqual('101B / 1kB')

        self.bar.step = 1024 * 501
        self.bar.steps = 1024 * 1024 * 11.2
        self.assertRenderedWidgetEqual('501kB / 11.2MB')

        self.bar.step = 1024 * 1024 * 908
        self.bar.steps = 1024 * 1024 * 1024 * 2.34
        self.assertRenderedWidgetEqual('908.0MB / 2.34G')


class TestBarWidget(TestBaseWidget):
    widget_class = frogress.BarWidget
    widget_attrs = {'width': 10, 'fill_char': '#', 'empty_char': '.'}

    def setUp(self):
        super(TestBarWidget, self).setUp()
        self.bar.finished = None

    def test_render_not_started(self):
        self.bar.started = None
        self.assertRenderedWidgetEqual('[..........]')

    def test_render(self):
        self.bar.get_percentage = mock.Mock(return_value=56.0)
        self.assertRenderedWidgetEqual('[#####.....]')

        self.bar.get_percentage = mock.Mock(return_value=60)
        self.assertRenderedWidgetEqual('[######....]')

        self.bar.get_percentage = mock.Mock(return_value=30.0)
        self.assertRenderedWidgetEqual('[###.......]')

        # bar should never be longer than it's width, even if > 100%
        self.bar.get_percentage = mock.Mock(return_value=230.0)
        self.assertRenderedWidgetEqual('[##########]')

    @mock.patch('frogress.bars.get_terminal_width')
    def test_render_len_not_known(self, get_terminal_width):
        get_terminal_width.return_value = None
        self.widget.width = 3
        self.bar = frogress.Bar(gen_range(5), widgets=[self.widget])
        self.bar.treshold = 0
        #self.bar.get_percentage = mock.Mock(return_value=None)
        self.bar.output = io.StringIO()
        list(self.bar) # exhaust progressbar iterator
        expected = ''.join('\r%s' % line for line in [
            '[#..]', # step 1
            '[.#.]', # step 2
            '[..#]', # step 3
            '[.#.]', # step 4
            '[#..]', # step 5
            '[###]', # bar.finish()
        ])
        self.assertEqual(self.bar.output.getvalue(), expected)


class TestTimerWidget(TestBaseWidget):
    widget_class = frogress.TimerWidget
    widget_attrs = {'prefix': 'Elapsed: '}

    def test_get_total_seconds(self):
        self.bar.get_timedelta = mock.Mock(return_value=None)
        self.assertEqual(self.widget.get_total_seconds(self.bar), 0)

    def test_render(self):
        minute = 60
        hour = 60 * minute

        self.widget.get_total_seconds = mock.Mock(return_value=0)
        self.assertRenderedWidgetEqual('Elapsed: 0.0s')

        self.widget.get_total_seconds = mock.Mock(return_value=4.8)
        self.assertRenderedWidgetEqual('Elapsed: 4.8s')

        self.widget.get_total_seconds = mock.Mock(return_value=12.349)
        self.assertRenderedWidgetEqual('Elapsed: 12.3s')

        self.widget.get_total_seconds = mock.Mock(return_value=62)
        self.assertRenderedWidgetEqual('Elapsed: 1min2s')

        seconds = hour * 2 + minute * 14 + 0.5
        self.widget.get_total_seconds = mock.Mock(return_value=seconds)
        self.assertRenderedWidgetEqual('Elapsed: 2h14min0s')

        seconds= hour * 28 + minute * 51
        self.widget.get_total_seconds = mock.Mock(return_value=seconds)
        self.assertRenderedWidgetEqual('Elapsed: 1d4h51min0s')


class TestWhirlWidget(TestBaseWidget):
    widget_class = frogress.WhirlWidget
    widget_attrs = {'chars': '12345', 'finished_text': 'Done'}

    def test_render(self):
        self.bar.finished = None
        self.assertRenderedWidgetEqual('1')
        self.assertEqual(self.widget.pos, 1)
        self.assertRenderedWidgetEqual('2')
        self.assertRenderedWidgetEqual('3')
        self.assertRenderedWidgetEqual('4')
        self.assertRenderedWidgetEqual('5')
        self.assertEqual(self.widget.pos, 5)
        self.assertRenderedWidgetEqual('1')
        self.assertRenderedWidgetEqual('2')
        self.assertEqual(self.widget.pos, 7)
        self.bar.finished = True
        self.assertRenderedWidgetEqual('Done')

class TestEtaWidget(TestBaseWidget):
    widget_class = frogress.EtaWidget
    widget_attrs = {'prefix': 'Eta: '}

    def test_render(self):
        self.bar.finished = None
        self.bar.get_timedelta = mock.Mock(return_value=10.0)
        self.bar.get_percentage = mock.Mock(return_value=25.0)
        self.assertRenderedWidgetEqual('Eta: 30.0s')

        self.bar.get_timedelta = mock.Mock(return_value=60*60*2.5)
        self.bar.get_percentage = mock.Mock(return_value=40.0)
        self.assertRenderedWidgetEqual('Eta: 3h45min0s')

        self.bar.started = None
        self.assertRenderedWidgetEqual('Eta: --')

        self.bar.finished = True
        self.assertRenderedWidgetEqual('Eta: --')

class TestWatchLenWidget(TestBaseWidget):
    widget_class = frogress.WatchLenWidget
    widget_attrs = {'prefix': 'Len: '}

    def test_render(self):
        self.bar.watch = [1,1,1]
        self.assertRenderedWidgetEqual('Len: 3')

        self.bar.watch = []
        self.assertRenderedWidgetEqual('Len: 0')

        self.bar.watch = set([1])
        self.assertRenderedWidgetEqual('Len: 1')

        self.bar.watch = {1:1, 2:2}
        self.assertRenderedWidgetEqual('Len: 2')

        self.bar.watch = None
        self.assertRenderedWidgetEqual('Len: --')
