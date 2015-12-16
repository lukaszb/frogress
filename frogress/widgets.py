from . import humanize


class Widget(object):

    def render(self, bar):
        raise NotImplementedError


class BarWidget(Widget):

    def __init__(self, width=10, fill_char='#', empty_char='.'):
        self.width = width
        self.fill_char = fill_char
        self.empty_char = empty_char
        self.pos = -1
        self.pos_delta = 1

    def render(self, bar):
        percentage = bar.get_percentage()
        if not bar.started:
            progress = self.empty_char * self.width
        elif bar.finished:
            progress = self.fill_char * self.width
        elif percentage is not None:
            filled_count = int(percentage * self.width / 100.0)
            filled = self.fill_char * min(filled_count, self.width)
            progress = filled.ljust(self.width, self.empty_char)
        else:
            self.pos += self.pos_delta
            if self.pos == self.width - 1:
                self.pos_delta = -1
            elif self.pos == 0:
                self.pos_delta = 1
            progress = [self.empty_char] * self.width
            progress[self.pos] = self.fill_char
            progress = ''.join(progress)
        return '[%s]' % progress


class WhirlWidget(Widget):
    finished_text = '*'

    def __init__(self, chars='|/-\\'):
        self.chars = chars
        self.pos = 0

    def render(self, bar):
        if bar.finished:
            progress = self.finished_text
        else:
            progress = self.chars[self.pos % len(self.chars)]
            self.pos += 1
        return progress


class PrefixWidget(Widget):
    default_prefix = None
    def __init__(self, prefix=None):
        self.prefix = prefix if prefix is not None else self.default_prefix


class ProgressWidget(PrefixWidget):
    default_prefix = 'Progress: '

    def render(self, bar):
        progress = '%s%s' % (self.prefix, bar.step)
        if bar.steps is not None:
            progress = '%s / %s' % (progress, bar.steps)
        return progress


class PercentageWidget(PrefixWidget):
    default_prefix = ''

    def render(self, bar):
        percentage = '%.1f%%' % bar.get_percentage()
        return '%s%s' % (self.prefix, percentage.rjust(6))


class TransferWidget(PrefixWidget):
    default_prefix = 'Transfer: '

    def render(self, bar):
        progress = '%s%s' % (self.prefix, humanize.size(bar.step))
        if bar.steps:
            progress = '%s / %s' % (progress, humanize.size(bar.steps))
        return progress


class TimerWidget(PrefixWidget):
    default_prefix = 'Time: '

    def get_total_seconds(self, bar):
        delta = bar.get_timedelta()
        if delta is not None:
            return delta
        return 0

    def render(self, bar):
        progress = humanize.time(self.get_total_seconds(bar))
        return ''.join((self.prefix, progress))


class EtaWidget(PrefixWidget):
    default_prefix = 'ETA: '

    def render(self, bar):
        percentage = bar.get_percentage()
        if not bar.started or not percentage or bar.finished:
            progress = '--'
        else:
            seconds = bar.get_timedelta()
            estimated_total = seconds * 100.0 / percentage
            progress = humanize.time(estimated_total - seconds)
        return ''.join((self.prefix, progress))


class WatchLenWidget(PrefixWidget):
    default_prefix = 'Len: '

    def render(self, bar):
        if bar.watch is None:
            length = '--'
        else:
            length = '%s' % (len(bar.watch),)
        return ''.join((self.prefix, length))
