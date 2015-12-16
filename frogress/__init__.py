"""
frogress is simple progress tool
"""
from .bars import Bar
from .bars import TransferBar
from .bars import WatchBar
from .bars import TransferWatchBar
from .api import bar
from .utils import get_iterable_size
from .utils import get_file_info
from .widgets import Widget
from .widgets import EtaWidget
from .widgets import PercentageWidget
from .widgets import ProgressWidget
from .widgets import TransferWidget
from .widgets import BarWidget
from .widgets import TimerWidget
from .widgets import WhirlWidget
from .widgets import WatchLenWidget


__all__ = [
    'Bar',
    'TransferBar',
    'WatchBar',
    'TransferWatchBar',
    'Widget',
    'EtaWidget',
    'PercentageWidget',
    'ProgressWidget',
    'TransferWidget',
    'BarWidget',
    'TimerWidget',
    'WhirlWidget',
    'WatchLenWidget',
    'get_file_info',
    'get_iterable_size',
    'bar',
]

VERSION = (0, 9, 1)

__version__ = '.'.join((str(each) for each in VERSION[:4]))

def get_version():
    """
    Returns shorter version (digit parts only) as string.
    """
    version = '.'.join((str(each) for each in VERSION[:3]))
    if len(VERSION) > 3:
        version += str(VERSION[3])
    return version

