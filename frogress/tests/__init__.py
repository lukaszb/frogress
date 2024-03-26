import os
import unittest


def collector():
    start_dir = os.path.abspath(os.path.dirname(__file__))
    return unittest.defaultTestLoader.discover(start_dir)

