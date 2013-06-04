from __future__ import unicode_literals
from .compat import unittest
import os


def collector():
    start_dir = os.path.abspath(os.path.dirname(__file__))
    return unittest.defaultTestLoader.discover(start_dir)

