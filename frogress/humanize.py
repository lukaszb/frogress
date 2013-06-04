KB = 1024.0
MB = 1024 * KB
GB = 1024 * MB

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR


def size(value, sep=''):
    gbytes = value / GB
    mbytes = value / MB
    kbytes = value / KB
    if gbytes >= 1:
        template = '%.2f{sep}G' % gbytes
    elif mbytes >= 1:
        template = '%.1f{sep}MB' % mbytes
    elif kbytes >= 1:
        template = '%i{sep}kB' % kbytes
    else:
        template = '%d{sep}B' % value
    return template.format(sep=sep)


def time(seconds):
    days = hours = minutes = 0
    template = ['{seconds:.1f}s']

    days = int(seconds / DAY)
    seconds %= DAY
    hours = int(seconds / HOUR)
    seconds %= HOUR
    minutes = int(seconds / MINUTE)
    seconds %= MINUTE

    if days:
        template = '{days}d{hours}h{minutes}min{seconds:.0f}s'
    elif hours:
        template = '{hours}h{minutes}min{seconds:.0f}s'
    elif minutes:
        template = '{minutes}min{seconds:.0f}s'
    else:
        template = '{seconds:.1f}s'
    return template.format(
        seconds=seconds,
        minutes=minutes,
        hours=hours,
        days=days,
    )

