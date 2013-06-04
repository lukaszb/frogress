#!/usr/bin/env python
import datetime
import frogress
import os
import time


DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sampledata')
sample_filename = lambda name: os.path.join(DATA_DIR, name)

def gen_range(count):
    # we use gen_range as range/xrange are inconsistant between Python 2/3
    num = 0
    while num < count:
        yield num
        num += 1


def show_progress(title, iterable, **kwargs):
    sleep = kwargs.pop('sleep', 0.01)
    timeout = kwargs.pop('timeout', 2)
    line = '  %s  ' % title
    print(line.center(80, '=') + '\n')
    started = datetime.datetime.now()
    for item in frogress.bar(iterable, **kwargs):
        if sleep:
            time.sleep(sleep)
        if (datetime.datetime.now() - started).total_seconds() > timeout:
            print('\n[Timeout reached: %.1fs]' % timeout)
            break
    print('\n')

def requests_progress():
    import requests
    import tempfile
    print('  requests  '.center(80, '=') + '\n')
    url = 'http://python.org/ftp/python/3.3.2/Python-3.3.2.tar.bz2'
    chunk_size = 2**16
    with tempfile.NamedTemporaryFile('w') as fout:
        response = requests.get(url, stream=True)
        stream = response.iter_content(chunk_size)
        bar = frogress.TransferBar(stream,
            steps=int(response.headers['content-length']),
            step_callback=fout.tell,
        )
        for chunk in bar:
            fout.write(chunk)
    print('\n')


def main():
    requests_progress()
    show_progress('Generator', gen_range(100))
    show_progress('List', range(80))
    show_progress('Generator (known total items count)', xrange(100), steps=100)
    show_progress('List', range(120))
    show_progress('Whirl', gen_range(150), widgets=[frogress.ProgressWidget,
        frogress.WhirlWidget])
    show_progress('A file', open(sample_filename('books.xml')), sleep=0.001)

    try:
        import gzip
        from lxml.etree import iterparse
        filename = sample_filename('books.xml.gz')
        xml_fin = gzip.open(filename)
        context = iterparse(xml_fin, tag='book')
        show_progress('Gzipped XML file', context, source=xml_fin.myfileobj)
    except ImportError:
        print("Cannot import lxml - won't show example :(")



if __name__ == '__main__':
    main()

