from . import widgets as w
from .bars import Bar
from .bars import TransferBar
from .utils import get_iterable_size
from .utils import get_file_info
from contextlib import contextmanager
from threading import Thread
import os


def bar(iterable, **kwargs):
    bar_cls = Bar
    kwargs.setdefault("steps", get_iterable_size(iterable))

    source = kwargs.pop("source", iterable)
    file_info = get_file_info(source)
    if file_info:
        kwargs["steps"] = file_info["size"]
        kwargs["step_callback"] = file_info["step_callback"]
        bar_cls = TransferBar

    progressbar = bar_cls(iterable, **kwargs)
    return progressbar


@contextmanager
def spinner(title, done="Done", title_on_done=None):
    finished = False

    def gen():
        finished
        while not finished:
            yield

    chars = '⣾⣽⣻⢿⡿⣟⣯⣷'
    chars = '⡀⡁⡂⡃⡄⡅⡆⡇⡈⡉⡊⡋⡌⡍⡎⡏⡐⡑⡒⡓⡔⡕⡖⡗⡘⡙⡚⡛⡜⡝⡞⡟⡠⡡⡢⡣⡤⡥⡦⡧⡨⡩⡪⡫⡬⡭⡮⡯⡰⡱⡲⡳⡴⡵⡶⡷⡸⡹⡺⡻⡼⡽⡾⡿⢀⢁⢂⢃⢄⢅⢆⢇⢈⢉⢊⢋⢌⢍⢎⢏⢐⢑⢒⢓⢔⢕⢖⢗⢘⢙⢚⢛⢜⢝⢞⢟⢠⢡⢢⢣⢤⢥⢦⢧⢨⢩⢪⢫⢬⢭⢮⢯⢰⢱⢲⢳⢴⢵⢶⢷⢸⢹⢺⢻⢼⢽⢾⢿⣀⣁⣂⣃⣄⣅⣆⣇⣈⣉⣊⣋⣌⣍⣎⣏⣐⣑⣒⣓⣔⣕⣖⣗⣘⣙⣚⣛⣜⣝⣞⣟⣠⣡⣢⣣⣤⣥⣦⣧⣨⣩⣪⣫⣬⣭⣮⣯⣰⣱⣲⣳⣴⣵⣶⣷⣸⣹⣺⣻⣼⣽⣾⣿'
    def task():
        abar = bar(
            gen(),
            widgets=[w.TemplateWidget(title), w.WhirlWidget(chars=chars, finished_text=done)],
            separator=" ",
        )
        list(abar)

    thread = Thread(target=task)
    thread.start()
    try:
        yield
        finished = True
    finally:
        thread.join()
        if title_on_done:
            line = "\r%s" % title_on_done
            width = os.get_terminal_size().columns
            print(line.rjust(width))
        else:
            print()
        pass
