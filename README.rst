=====================================
frogress - a progress tool for humans
=====================================

.. image:: https://secure.travis-ci.org/lukaszb/frogress.png?branch=master
   :target: http://travis-ci.org/lukaszb/frogress

.. image:: https://coveralls.io/repos/lukaszb/frogress/badge.png?branch=master
   :target: https://coveralls.io/r/lukaszb/frogress/

.. image:: https://pypip.in/v/frogress/badge.png
   :target: https://crate.io/packages/frogress/

::

                /----------------------------------------------------------------------------------\
                |                                                                                  |
      @..@     /| [###.......] Progress: 34.2MB / 125.8MB |  25.0% | Time: 14min3s | ETA: 19min52s |
     (----)   / |                                                                                  |
    ( >__< )    \----------------------------------------------------------------------------------/
    ^^ ~~ ^^


frogress is small progress indication tool to be used for fast prototyping.
Why *frogress* anyway? Because it's a bar (most of the time) and it jumps on
your terminal, that's why!

- Does NOT break your workflow (in most cases there is no need to call
  progress bar to render itself)
- It can guess if you `iterate over a list`_ (or similar iterable) ...
- or if iterate over a file ...
- or if iterate over generator - provided you know it's total length ...
- or used within a ``with`` context manager ...
- or not! (no eta, no total steps, no percentage and indicator instead of a bar
  but it works!)
- And you can easily teach it how to show progress of fat, gzipped xml file
  when using lxml_ to parse it
- Supports Python 2.6+, Python 3, PyPY
- Fully tested


Iteration examples
==================


.. _iterate over a list:

Iterate over a list
-------------------

::

    >>> import frogress
    >>> items = [1, 2, 3, 4, 5]
    >>> for item in frogress.bar(items):
    ...     pass # do something with item

    [##........] Step 2/5 |  20.0% | Time: 0.1s | ETA: 0.5s


Iterate over a file
-------------------

::

    >>> import frogress
    >>> for line in frogress.bar(open('/path/to/file', steps_label='Progress')):
    ...     pass # do something cruel with a line

    [###.......] Progress: 3.2MB / 12.8MB |  25.0% | Time: 14min3s | ETA: 19min52s


Iterate over generator
----------------------

::

    >>> import frogress
    >>> count = 100
    >>> items = range(count)
    >>> for item in frogress.bar(items, steps=count):
    ...     pass # do something with item

    [#########.] Step 86/100 |  86.0% | Time: 1.2s | ETA: 7.3s


Iterate over a generator with unknown total number of steps
-----------------------------------------------------------

::

    >>> import frogress
    >>> def counter():
    ...     num = 1
    ...     while True:
    ...         yield num
    ...         num += 1
    ...
    >>> items = counter()
    >>> for item in frogress.bar(items):
    ...     pass # do something with item

    [........#.] Step: 1410 | Time: 2min14s
    [.........#] Step: 1411 | Time: 2min15s
    [........#.] Step: 1412 | Time: 2min16s
    [.......#..] Step: 1413 | Time: 2min17s


Iterate over a file with a ``with`` context
-------------------------------------------

::

    >>> import frogress
    >>> with frogress.bar(open('/path/to/file', steps_label='Progress')) as f:
    ...     for line in f:
    ...         pass # do something cruel with a line

    [###.......] Progress: 3.2MB / 12.8MB |  25.0% | Time: 14min3s | ETA: 19min52s



Iterate over gzipped xml file using lxml
----------------------------------------

The only problem with how to present a progress of file that's being processed
is the source from which frogress should extract progress information. We can
try to do this simple way (without knowledge of how much of the file is already
processed) or give ``frogress`` a *source*.


Simple way
~~~~~~~~~~

::

    >>> import frogress
    >>> import gzip
    >>> from lxml.etree import iterparse
    >>> stream = gzip.open('my-fat.xml.gz')
    >>> context = iterparse(stream)
    >>> for action, element in frogress.bar(context):
    ...     pass # do something with element
    ...     element.clear() # don't forget about the memory!

    [...#......] Progress: 41923 | Time: 1h42min

This is perfectly fine: we passed an iterable that doesn't provide information
on how many total items there is to process - so we have an bar activity
indicator, no total steps at the progress and no ETA.

However, there is clearly a way of retrieving this information - after all this
is only a file that's being processed. And that file should be passed as
``source`` argument to the ``frogress.bar`` function.

Pass source
~~~~~~~~~~~

::

    >>> import frogress
    >>> import gzip
    >>> from lxml.etree import iterparse
    >>> stream = gzip.open('my-fat.xml.gz')
    >>> context = iterparse(stream)
    >>> for action, element in frogress.bar(context, source=stream.myfileobj):
    ...     pass # do something with element
    ...     element.clear() # don't forget about the memory!

    [#####.....] Progress: 73.5MB / 156.4MB |  47.3% | Time: 1h42min | ETA: 1h53min

Just remember to pass file that is actually processed, not a wrapper! Standard
file would be passed directly, however in example, ``gzip`` module wraps stream
it is working on and it's available as attribute ``myfileobj``. On the other
hand ``bz2`` module doesn't wrap streams. And so on. ``frogress`` can guess if
a stream is file like object, however passing proper source is responsibility
of the user.


Progress bar class API
======================

Most of the time you won't need to call those API directly - ``frogress.bar``
function should work for majority of the use cases. If, however, you feel like
you need to make some customization, here we present some examples::

    >>> import frogress
    >>> items = [1, 2, 3, 4, 5]
    >>> progressbar = frogress.Bar(items)
    >>> progressbar.step
    0
    >>> progressbar.started # it's still None
    >>> progressbar.finished # here too
    >>> for item in progressbar:
    ...     pass # process the item (it will draw progressbar during iteration)
    >>> progressbar.step
    5
    >>> progressbar.widgets
    [<BarWidget>, <ProgressWidget>, <PercentageWidget>, <EtaWidget>, <TimeWidget>]
    >>> len(progressbar)
    5
    >>> progressbar.output
    <open file '<stderr>', mode 'w' at 0x103df61e0>
    >>> progressbar.started
    datetime.datetime(2013, 5, 12, 22, 2, 26, 752454)
    >>> progressbar.finished
    datetime.datetime(2013, 5, 12, 22, 2, 26, 792901)


Tips & Tricks
=============

How to change label of the progress widget
------------------------------------------

::

    >>> import frogress
    >>> items = [1, 2, 3, 4, 5]
    >>> widgets = [frogress.BarWidget, frogress.ProgressWidget('Items: '), frogress.TimerWidget]
    >>> for item in frogress.bar(items, widgets=widgets):
    >>>     pass


.. _lxml: http://lxml.de/

