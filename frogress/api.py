from .bars import Bar
from .bars import TransferBar
from .utils import get_iterable_size
from .utils import get_file_info


def bar(iterable, **kwargs):
    bar_cls = Bar
    kwargs.setdefault('steps', get_iterable_size(iterable))

    source = kwargs.pop('source', iterable)
    file_info = get_file_info(source)
    if file_info:
        kwargs['steps'] = file_info['size']
        kwargs['step_callback'] = file_info['step_callback']
        bar_cls = TransferBar

    progressbar = bar_cls(iterable, **kwargs)
    return progressbar

