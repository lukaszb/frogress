import sys

__all__ = ['unittest']

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

