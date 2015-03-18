try:
    import psutil
except ImportError:
    print "Module 'psutil' required"

try:
    import os
except ImportError:
    print "Requirement: 'os' module not found."

try:
    import time
except ImportError:
    print "Requirement: 'time' module not found."

from .common import determine_status

FREQ = 10

IO_READ_COUNT_WARN = None
IO_WRITE_COUNT_WARN = None
IO_READ_BYTES_WARN = None
IO_WRITE_BYTES_WARN = None
IO_READ_TIME_WARN = None
IO_WRITE_TIME_WARN = None

IO_READ_COUNT_CRIT = None
IO_WRITE_COUNT_CRIT = None
IO_READ_BYTES_CRIT = None
IO_WRITE_BYTES_CRIT = None
IO_READ_TIME_CRIT = None
IO_WRITE_TIME_CRIT = None

IO_READ_COUNT_TRIGGER = None
IO_WRITE_COUNT_TRIGGER = None
IO_READ_BYTES_TRIGGER = None
IO_WRITE_BYTES_TRIGGER = None
IO_READ_TIME_TRIGGER = None
IO_WRITE_TIME_TRIGGER = None


USAGE_TOTAL_WARN = None
USAGE_USED_WARN = None
USAGE_FREE_WARN = None
USAGE_PERCENT_WARN = None

USAGE_TOTAL_CRIT = None
USAGE_USED_CRIT = None
USAGE_FREE_CRIT = None
USAGE_PERCENT_CRIT = None

USAGE_TOTAL_TRIGGER = None
USAGE_USED_TRIGGER = None
USAGE_FREE_TRIGGER = None
USAGE_PERCENT_TRIGGER = None


cached_data = {}


def parse_settings_disk_usage(settings):
    _settings = {
        'total': {},
        'used': {},
        'free': {},
        'percent': {},
        'freq': settings['freq'] if 'freq' in settings else FREQ
    }

    # Triggers
    _settings['total']['trigger'] = settings['total']['trigger'] \
        if 'total' in settings and 'trigger' in settings['total'] else USAGE_TOTAL_TRIGGER

    _settings['used']['trigger'] = settings['used']['trigger'] \
        if 'used' in settings and 'trigger' in settings['used'] else USAGE_USED_TRIGGER

    _settings['free']['trigger'] = settings['free']['trigger'] \
        if 'free' in settings and 'trigger' in settings['free'] else USAGE_FREE_TRIGGER

    _settings['percent']['trigger'] = settings['percent']['trigger'] \
        if 'percent' in settings and 'trigger' in settings['percent'] else USAGE_PERCENT_TRIGGER

    # Warning Threshold
    _settings['total']['warn'] = settings['total']['warn'] \
        if 'total' in settings and 'warn' in settings['total'] else USAGE_TOTAL_WARN

    _settings['used']['warn'] = settings['used']['warn'] \
        if 'used' in settings and 'warn' in settings['used'] else USAGE_USED_WARN

    _settings['free']['warn'] = settings['free']['warn'] \
        if 'free' in settings and 'warn' in settings['free'] else USAGE_FREE_WARN

    _settings['percent']['warn'] = settings['percent']['warn'] \
        if 'percent' in settings and 'warn' in settings['percent'] else USAGE_PERCENT_WARN

    # Critical Threshold
    _settings['total']['crit'] = settings['total']['crit'] \
        if 'total' in settings and 'crit' in settings['total'] else USAGE_TOTAL_CRIT

    _settings['used']['crit'] = settings['used']['crit'] \
        if 'used' in settings and 'crit' in settings['used'] else USAGE_USED_CRIT

    _settings['free']['crit'] = settings['free']['crit'] \
        if 'free' in settings and 'crit' in settings['free'] else USAGE_FREE_CRIT

    _settings['percent']['crit'] = settings['percent']['crit'] \
        if 'percent' in settings and 'crit' in settings['percent'] else USAGE_PERCENT_CRIT

    # Tags
    _settings['total']['tags'] = settings['total']['tags'] + ['disk'] \
        if 'total' in settings and 'tags' in settings['total'] else ['disk']

    _settings['used']['tags'] = settings['used']['tags'] + ['disk'] \
        if 'used' in settings and 'tags' in settings['used'] else ['disk']

    _settings['free']['tags'] = settings['free']['tags'] + ['disk'] \
        if 'free' in settings and 'tags' in settings['free'] else ['disk']

    _settings['percent']['tags'] = settings['percent']['tags'] + ['disk'] \
        if 'percent' in settings and 'tags' in settings['percent'] else ['disk']

    return _settings


def parse_settings_disk_io(settings):
    _settings = {
        'read_count': {},
        'write_count': {},
        'read_bytes': {},
        'write_bytes': {},
        'read_time': {},
        'write_time': {},
        'freq': settings['freq'] if 'freq' in settings else FREQ
    }


    # Triggers
    _settings['read_count']['trigger'] = settings['read_count']['trigger'] \
        if 'read_count' in settings and 'trigger' in settings['read_count'] else IO_READ_COUNT_TRIGGER

    _settings['write_count']['trigger'] = settings['write_count']['trigger'] \
        if 'write_count' in settings and 'trigger' in settings['write_count'] else IO_WRITE_COUNT_TRIGGER

    _settings['read_bytes']['trigger'] = settings['read_bytes']['trigger'] \
        if 'read_bytes' in settings and 'trigger' in settings['read_bytes'] else IO_READ_BYTES_TRIGGER

    _settings['write_bytes']['trigger'] = settings['write_bytes']['trigger'] \
        if 'write_bytes' in settings and 'trigger' in settings['write_bytes'] else IO_WRITE_BYTES_TRIGGER

    _settings['read_time']['trigger'] = settings['read_time']['trigger'] \
        if 'read_time' in settings and 'trigger' in settings['read_time'] else IO_READ_TIME_TRIGGER

    _settings['write_time']['trigger'] = settings['write_time']['trigger'] \
        if 'write_time' in settings and 'trigger' in settings['write_time'] else IO_WRITE_TIME_TRIGGER

    # Warning threashold
    _settings['read_count']['warn'] = settings['read_count']['warn'] \
        if 'read_count' in settings and 'warn' in settings['read_count'] else IO_READ_COUNT_WARN

    _settings['write_count']['warn'] = settings['write_count']['warn'] \
        if 'write_count' in settings and 'warn' in settings['write_count'] else IO_WRITE_COUNT_WARN

    _settings['read_bytes']['warn'] = settings['read_bytes']['warn'] \
        if 'read_bytes' in settings and 'warn' in settings['read_bytes'] else IO_READ_BYTES_WARN

    _settings['write_bytes']['warn'] = settings['write_bytes']['warn'] \
        if 'write_bytes' in settings and 'warn' in settings['write_bytes'] else IO_WRITE_BYTES_WARN

    _settings['read_time']['warn'] = settings['read_time']['warn'] \
        if 'read_time' in settings and 'warn' in settings['read_time'] else IO_READ_TIME_WARN

    _settings['write_time']['warn'] = settings['write_time']['warn'] \
        if 'write_time' in settings and 'warn' in settings['write_time'] else IO_WRITE_TIME_WARN

    # Critical threashold
    _settings['read_count']['crit'] = settings['read_count']['crit'] \
        if 'read_count' in settings and 'crit' in settings['read_count'] else IO_READ_COUNT_CRIT

    _settings['write_count']['crit'] = settings['write_count']['crit'] \
        if 'write_count' in settings and 'crit' in settings['write_count'] else IO_WRITE_COUNT_CRIT

    _settings['read_bytes']['crit'] = settings['read_bytes']['crit'] \
        if 'read_bytes' in settings and 'crit' in settings['read_bytes'] else IO_READ_BYTES_CRIT

    _settings['write_bytes']['crit'] = settings['write_bytes']['crit'] \
        if 'write_bytes' in settings and 'crit' in settings['write_bytes'] else IO_WRITE_BYTES_CRIT

    _settings['read_time']['crit'] = settings['read_time']['crit'] \
        if 'read_time' in settings and 'crit' in settings['read_time'] else IO_READ_TIME_CRIT

    _settings['write_time']['crit'] = settings['write_time']['crit'] \
        if 'write_time' in settings and 'crit' in settings['write_time'] else IO_WRITE_TIME_CRIT

    # Tags
    _settings['read_count']['tags'] = settings['read_count']['tags'] + ['disk'] \
        if 'read_count' in settings and 'tags' in settings['read_count'] else ['disk']

    _settings['write_count']['tags'] = settings['write_count']['tags'] + ['disk'] \
        if 'write_count' in settings and 'tags' in settings['write_count'] else ['disk']

    _settings['read_bytes']['tags'] = settings['read_bytes']['tags'] + ['disk'] \
        if 'read_bytes' in settings and 'tags' in settings['read_bytes'] else ['disk']

    _settings['write_bytes']['tags'] = settings['write_bytes']['tags'] + ['disk'] \
        if 'write_bytes' in settings and 'tags' in settings['write_bytes'] else ['disk']

    _settings['read_time']['tags'] = settings['read_time']['tags'] + ['disk'] \
        if 'read_time' in settings and 'tags' in settings['read_time'] else ['disk']

    _settings['write_time']['tags'] = settings['write_time']['tags'] + ['disk'] \
        if 'write_time' in settings and 'tags' in settings['write_time'] else ['disk']

    return _settings



def disk_io(settings=None):
    """ Return statistics on mounted system disks
    """
    global cached_data

    disk_info = []
    disks = [disk.device.split('/')[-1:][0] for disk in psutil.disk_partitions()]
    disk_io = psutil.disk_io_counters(perdisk=True)

    for device, info in disk_io.iteritems():

        if device not in disks:
            continue

        for type, metric in info.__dict__.iteritems():

            if '{type}.{dev}'.format(type=type, dev=device) not in cached_data:
                current_metric = 0
            else:
                current_metric = (metric - cached_data['{type}.{dev}'.format(type=type, dev=device)]) / settings['freq  ']

            cached_data['{type}.{dev}'.format(type=type, dev=device)] = metric

            data = {
                'host': os.uname()[1],
                'service': 'disk_io.{device}.{type}'.format(device=device, type=type),
                'metric': current_metric,
                'state': determine_status('disk_io.{type}'.format(type=type), metric,
                                          settings['{type}'.format(type=type)]['warn'],
                                          settings['{type}'.format(type=type)]['crit'],
                                          settings['{type}'.format(type=type)]['trigger']),
                'time': int(time.time()),
                'tags': settings['{type}'.format(type=type)]['tags'],
            }

            disk_info.append(data)

    return disk_info


def disk_usage(settings=None):
    """
    Return statistics on mounted system disks
    """

    disk_info = []
    disks = psutil.disk_partitions()

    for disk in disks:
        space = psutil.disk_usage(disk.mountpoint)
        for type, metric in space.__dict__.iteritems():

            data = {
                'host': os.uname()[1],
                'service': 'disk_usage.{device}.{type}'.format(device=disk.device.split('/')[-1:][0], type=type),
                'metric': metric,
                'state': determine_status('disk_usage.{type}'.format(type=type), metric,
                                          settings['{type}'.format(type=type)]['warn'],
                                          settings['{type}'.format(type=type)]['crit'],
                                          settings['{type}'.format(type=type)]['trigger']),
                'time': int(time.time()),
                'tags': settings['{type}'.format(type=type)]['tags'],
            }
            disk_info.append(data)

    return disk_info
