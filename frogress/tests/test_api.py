from __future__ import unicode_literals, absolute_import
from frogress.tests.compat import unittest
import frogress
import tempfile


class TestBar(unittest.TestCase):

    def test_bar_passes_parameters(self):
        seq = [1, 2, 3, 4, 5]
        progressbar = frogress.bar(seq)
        self.assertEqual(progressbar.iterable, seq)

    def test_file(self):
        with tempfile.NamedTemporaryFile('w') as tmp:
            text = 'foobar\n' * 25
            tmp.write(text)
            tmp.flush()
            f = open(tmp.name)
            bar = frogress.bar([], source=f)
            self.assertIsInstance(bar, frogress.TransferBar)
            self.assertEqual(bar.step_callback, f.tell)
            self.assertEqual(bar.steps, len(text))

