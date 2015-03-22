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

DEFAULT_TAGS = ['disk']
_settings = {
    'disk_usage': {
        'freq': 10,
        'total': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'used': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'free': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'percent': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS}
    },
    'disk_io': {
        'freq': 10,
        'read_count': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'write_count': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'read_bytes': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'write_bytes': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'read_time': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'write_time': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS}
    }
}


def disk_io(settings=None):
    """
    Return statistics on mounted system disks
    """
    global cached_data

    default_settings = _settings['disk_io']

    disk_info = []
    disks = [disk.device.split('/')[-1:][0] for disk in psutil.disk_partitions()]
    disk_io = psutil.disk_io_counters(perdisk=True)

    for device, info in disk_io.iteritems():

        if device not in disks:
            continue

        for metric_name, metric in info.__dict__.iteritems():

            do_run = True

            if '{metric_name}.{dev}'.format(metric_name=metric_name, dev=device) not in cached_data:
                do_run = False
                current_metric = 0
            else:
                current_metric = (metric - cached_data['{metric_name}.{dev}'.format(metric_name=metric_name, dev=device)]) / settings['freq']

            cached_data['{metric_name}.{dev}'.format(metric_name=metric_name, dev=device)] = metric

            data = {
                'host': os.uname()[1],
                'service': 'disk_io.{device}.{metric_name}'.format(device=device, metric_name=metric_name),
                'metric': current_metric,
                'state': determine_status('disk_io.{metric_name}'.format(metric_name=metric_name), current_metric,
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('warn',default_settings['{metric_name}'.format(metric_name=metric_name)]['warn']),
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('crit',default_settings['{metric_name}'.format(metric_name=metric_name)]['crit']),
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('trigger', default_settings['{metric_name}'.format(metric_name=metric_name)]['trigger'])),
                'time': int(time.time()),
                'tags': settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('tags', []) + default_settings['{metric_name}'.format(metric_name=metric_name)]['tags']
            }

            if do_run:
                disk_info.append(data)

            data = {
                'host': os.uname()[1],
                'service': 'disk_io.{device}.{metric_name}.raw'.format(device=device, metric_name=metric_name),
                'metric': metric,
                'state': determine_status('disk_io.{metric_name}'.format(metric_name=metric_name), current_metric,
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('warn',default_settings['{metric_name}'.format(metric_name=metric_name)]['warn']),
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('crit',default_settings['{metric_name}'.format(metric_name=metric_name)]['crit']),
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('trigger', default_settings['{metric_name}'.format(metric_name=metric_name)]['trigger'])),
                'time': int(time.time()),
                'tags': settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('tags', []) + default_settings['{metric_name}'.format(metric_name=metric_name)]['tags']
            }

            if do_run:
                disk_info.append(data)

    return disk_info


def disk_usage(settings=None):
    """
    Return statistics on mounted system disks
    """

    default_settings = _settings['disk_usage']

    disk_info = []
    disks = psutil.disk_partitions()

    for disk in disks:
        space = psutil.disk_usage(disk.mountpoint)
        for metric_name, metric in space.__dict__.iteritems():

            data = {
                'host': os.uname()[1],
                'service': 'disk_usage.{device}.{metric_name}'.format(device=disk.device.split('/')[-1:][0], metric_name=metric_name),
                'metric': metric,
                'state': determine_status('disk_usage.{metric_name}'.format(metric_name=metric_name), metric,
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('warn',default_settings['{metric_name}'.format(metric_name=metric_name)]['warn']),
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('crit',default_settings['{metric_name}'.format(metric_name=metric_name)]['crit']),
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('trigger', default_settings['{metric_name}'.format(metric_name=metric_name)]['trigger'])),
                'time': int(time.time()),
                'tags': settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('tags', []) + default_settings['{metric_name}'.format(metric_name=metric_name)]['tags']
            }
            disk_info.append(data)

    return disk_info
