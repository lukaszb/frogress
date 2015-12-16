from .bars import Bar
from .bars import TransferBar
from .bars import WatchBar
from .bars import TransferWatchBar
from .utils import get_iterable_size
from .utils import get_file_info


def bar(iterable, **kwargs):
    bar_cls = Bar
    kwargs.setdefault('steps', get_iterable_size(iterable))
    
    is_watching = 'watch' in kwargs
    print(kwargs, is_watching)
    
    source = kwargs.pop('source', iterable)
    file_info = get_file_info(source)
    
    if file_info:
        kwargs['steps'] = file_info['size']
        kwargs['step_callback'] = file_info['step_callback']
        if is_watching:
            bar_cls = TransferWatchBar
        else:
            bar_cls = TransferBar
    elif is_watching:
            bar_cls = WatchBar

    progressbar = bar_cls(iterable, **kwargs)
    return progressbar

