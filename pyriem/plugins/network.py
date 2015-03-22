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

DEFAULT_TAGS = ['network']

_settings = {
    'network_io': {
        'freq': 10,
        'bytes_sent': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'bytes_recv': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'packets_sent': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'packets_recv': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'errin': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'errout': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'dropin': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'dropout': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS
        }
    }
}

cached_data = {}

def network_io(settings=None):
    global cached_data

    default_settings = _settings['network_io']

    device_info = []

    net_io = psutil.net_io_counters(pernic=True)

    for device, vals in net_io.iteritems():
        for metric_name, metric in vals.__dict__.iteritems():
            do_run = True
            if '{metric_name}.{dev}'.format(metric_name=metric_name, dev=device) not in cached_data:
                current_metric = 0
                do_run = False
            else:
                current_metric = (metric - cached_data[
                    '{metric_name}.{dev}'.format(metric_name=metric_name, dev=device)]) / float(
                    settings.get('freq'))

            cached_data['{metric_name}.{dev}'.format(metric_name=metric_name, dev=device)] = metric

            data = {
                'host': os.uname()[1],
                'service': 'network_io.{device}.{metric_name}'.format(device=device, metric_name=metric_name),
                'metric': current_metric,
                'state': determine_status('network_io.{metric_name}'.format(metric_name=metric_name), current_metric,
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('warn',default_settings['{metric_name}'.format(metric_name=metric_name)]['warn']),
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('crit',default_settings['{metric_name}'.format(metric_name=metric_name)]['crit']),
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('trigger', default_settings['{metric_name}'.format(metric_name=metric_name)]['trigger'])),
                'time': int(time.time()),
                'tags': settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('tags', []) + default_settings['{metric_name}'.format(metric_name=metric_name)]['tags']
            }

            if do_run:
                device_info.append(data)

            data = {
                'host': os.uname()[1],
                'service': 'network_io.{device}.{metric_name}.raw'.format(device=device, metric_name=metric_name),
                'metric': metric,
                'state': determine_status('network_io.{metric_name}'.format(metric_name=metric_name), current_metric,
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('warn',default_settings['{metric_name}'.format(metric_name=metric_name)]['warn']),
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('crit',default_settings['{metric_name}'.format(metric_name=metric_name)]['crit']),
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('trigger', default_settings['{metric_name}'.format(metric_name=metric_name)]['trigger'])),
                'time': int(time.time()),
                'tags': settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('tags', []) + default_settings['{metric_name}'.format(metric_name=metric_name)]['tags']
            }

            if do_run:
                device_info.append(data)

    return device_info
