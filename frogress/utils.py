import os


DEFAULT_TERMINAL_WIDTH = 80


def get_list(count):
    return list(range(count))


def gen_range(count):
    num = 0
    while num < count:
        yield num
        num += 1


def get_terminal_width():
    try:
        return os.get_terminal_size().columns
    except OSError:
        return DEFAULT_TERMINAL_WIDTH


def get_first_attr(obj, attrs):
    for attr in attrs:
        if hasattr(obj, attr):
            return getattr(obj, attr)
    return None


def get_file_info(obj):
    if all(hasattr(obj, attr) for attr in ['seek', 'tell', 'fileno']):
        filename = get_first_attr(obj, ['filename', 'name'])
        if filename:
            return {
                'filename': filename,
                'size': os.path.getsize(filename),
                'step_callback': obj.tell,
            }
    return None


def get_iterable_size(iterable):
    if hasattr(iterable, '__len__'):
        return len(iterable)
    return None

