from __future__ import unicode_literals, absolute_import
from frogress.tests.compat import unittest
import frogress
import tempfile


class TestBar(unittest.TestCase):

    def test_bar_passes_parameters(self):
        seq = [1, 2, 3, 4, 5]
        progressbar = frogress.bar(seq)
        self.assertIs(progressbar.iterable, seq)

    def test_file(self):
        seq = [1, 2, 3, 4, 5]
        with tempfile.NamedTemporaryFile('w') as tmp:
            text = 'foobar\n' * 25
            tmp.write(text)
            tmp.flush()
            f = open(tmp.name)
            bar = frogress.bar(seq, source=f)
            self.assertIsInstance(bar, frogress.TransferBar)
            self.assertEqual(bar.step_callback, f.tell)
            self.assertEqual(bar.steps, len(text))
            self.assertIs(bar.iterable, seq)

    def test_watch(self):
        seq = [1, 2, 3, 4, 5]
        w = lambda: 1
        bar = frogress.bar(seq, watch=w)
        self.assertIsInstance(bar, frogress.WatchBar)
        self.assertEqual(bar.watch, w)
        self.assertIs(bar.iterable, seq)

    def test_watch_file(self):
        seq = [1, 2, 3, 4, 5]
        w = lambda: 1
        with tempfile.NamedTemporaryFile('w') as tmp:
            text = 'foobar\n' * 25
            tmp.write(text)
            tmp.flush()
            f = open(tmp.name)
            bar = frogress.bar(seq, watch=w, source=f)
            self.assertIsInstance(bar, frogress.TransferWatchBar)
            self.assertIs(bar.watch, w)
            self.assertEqual(bar.step_callback, f.tell)
            self.assertEqual(bar.steps, len(text))
            self.assertIs(bar.iterable, seq)
