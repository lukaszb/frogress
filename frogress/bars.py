from __future__ import unicode_literals
from __future__ import print_function
from .utils import get_terminal_width
from .widgets import BarWidget
from .widgets import EtaWidget
from .widgets import ProgressWidget
from .widgets import TimerWidget
from .widgets import TransferWidget
from .widgets import PercentageWidget
import datetime
import sys
import time


class Bar(object):

    DEFAULT_WIDGETS = [BarWidget, ProgressWidget, TimerWidget, EtaWidget]

    def __init__(self, iterable, steps=None, step_callback=None, widgets=None):
        self.steps = steps
        self.iterable = iterable
        self.step = 0
        self.step_callback = step_callback
        self.started = None
        self.finished = None
        self.setup_widgets(widgets)
        self.separator = ' | '
        self.output = sys.stdout
        self.last_shown_at = None
        self.treshold = 0.05 # in seconds

    def setup_widgets(self, widgets):
        _widgets = widgets or self.DEFAULT_WIDGETS[:]
        if widgets is None and self.steps:
            _widgets.insert(0, PercentageWidget())
        self.widgets = [w() if callable(w) else w for w in _widgets]

    @property
    def step(self):
        if self.step_callback:
            return self.step_callback()
        return self._step

    @step.setter
    def step(self, step):
        self._step = step

    @property
    def iterable(self):
        return self._iterable

    @iterable.setter
    def iterable(self, iterable):
        self._iterable = iterable
        self.iterator = iter(iterable)

    def __iter__(self):
        # bar itself is an iterator already
        return self

    def __next__(self):
        if not self.started:
            self.start()
        try:
            item = next(self.iterator)
            self.step += 1
            self.show()
            return item
        except StopIteration:
            self.finish()
            raise

    next = __next__

    def start(self):
        self.started = datetime.datetime.now()

    def finish(self):
        self.finished = datetime.datetime.now()
        self.show()

    def get_timedelta(self, now=None):
        """
        Returns number of seconds that passed since ``self.started``, as float.
        None is returned if ``self.started`` was not set yet.
        """
        def datetime_to_time(timestamp):
            atime = time.mktime(timestamp.timetuple())
            atime += timestamp.microsecond / 10.0**6
            return atime
        if self.started is not None:
            now = now or datetime.datetime.now()
            started_time = datetime_to_time(self.started)
            now_time = datetime_to_time(now)
            return now_time - started_time
        return None

    def render_element(self, element):
        if hasattr(element, 'render'):
            return element.render(self)
        else:
            return element

    def render(self):
        """
        Returns whole information on the progress for the current's bar state,
        as a string.
        """
        elements = [self.render_element(e) for e in self.widgets]
        progressbar = self.separator.join(elements)
        width = get_terminal_width()
        if width:
            # leave last column for cursor
            progressbar = progressbar.ljust(width - 1)
        return progressbar

    def _show(self):
        self.last_shown_at = datetime.datetime.now()
        text = '\r%s' % self.render()
        self.output.write(text)
        self.output.flush()

    def show(self, now=None):
        now = now or datetime.datetime.now()
        delta = datetime.timedelta(seconds=self.treshold)
        should_show = any((
            self.finished,
            not self.last_shown_at,
            not self.treshold,
            self.treshold and self.last_shown_at and (now - self.last_shown_at) > delta,
        ))
        if should_show:
            self._show()

    def get_percentage(self):
        if not self.steps:
            return None
        return self.step * 100.0 / self.steps


class TransferBar(Bar):
    DEFAULT_WIDGETS = [BarWidget, TransferWidget, TimerWidget, EtaWidget]

