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


DEFAULT_TAGS = ['memory']

_settings = {
    'virtual_memory': {
        'freq': 10,
        'total': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'available': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'percent': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'used': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'free': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'active': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'inactive': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'buffers': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'cached': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS}
    },
    'swap_memory': {
        'freq': 10,
        'total': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'percent': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'used': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'free': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'sin': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'sout': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS}
    }
}


def virtual_memory(settings):
    """
    Virtual memory collector
    """

    default_settings = _settings['virtual_memory']
    virtual_memory = psutil.virtual_memory()
    return_data = []

    try:
        for item in virtual_memory.__dict__.iteritems():
            metric_name = item[0]
            metric = item[1]

            data = {
                'host': os.uname()[1],
                'service': 'virtual_memory.{metric_name}'.format(metric_name=metric_name),
                'metric': metric,
                'state': determine_status('network_io.{metric_name}'.format(metric_name=metric_name), metric,
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('warn',default_settings['{metric_name}'.format(metric_name=metric_name)]['warn']),
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('crit',default_settings['{metric_name}'.format(metric_name=metric_name)]['crit']),
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('trigger', default_settings['{metric_name}'.format(metric_name=metric_name)]['trigger'])),
                'time': int(time.time()),
                'tags': settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('tags', []) + default_settings['{metric_name}'.format(metric_name=metric_name)]['tags']
            }
            return_data.append(data)

    except AttributeError:

        for key, item in default_settings.iteritems():

            metric_name = key
            metric = virtual_memory.__getattribute__(item)

            data = {
                'host': os.uname()[1],
                'service': 'virtual_memory.{metric_name}'.format(metric_name=metric_name),
                'metric': metric,
                'state': determine_status('network_io.{metric_name}'.format(metric_name=metric_name), metric,
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('warn',default_settings['{metric_name}'.format(metric_name=metric_name)]['warn']),
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('crit',default_settings['{metric_name}'.format(metric_name=metric_name)]['crit']),
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('trigger', default_settings['{metric_name}'.format(metric_name=metric_name)]['trigger'])),
                'time': int(time.time()),
                'tags': settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('tags', []) + default_settings['{metric_name}'.format(metric_name=metric_name)]['tags']
            }

            if 'ttl' in settings:
                data['ttl'] = settings['ttl']

            return_data.append(data)

    return return_data


def swap_memory(settings):

    default_settings = _settings['swap_memory']

    swap_memory = psutil.swap_memory()

    return_data = []

    try:
        for item in swap_memory.__dict__.iteritems():
            metric_name = item[0]
            metric = item[1]

            data = {
                'host': os.uname()[1],
                'service': 'swap_memory.{metric_name}'.format(metric_name=metric_name),
                'metric': metric,
                'state': determine_status('network_io.{metric_name}'.format(metric_name=metric_name), metric,
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('warn',default_settings['{metric_name}'.format(metric_name=metric_name)]['warn']),
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('crit',default_settings['{metric_name}'.format(metric_name=metric_name)]['crit']),
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('trigger', default_settings['{metric_name}'.format(metric_name=metric_name)]['trigger'])),
                'time': int(time.time()),
                'tags': settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('tags', []) + default_settings['{metric_name}'.format(metric_name=metric_name)]['tags']
            }

            return_data.append(data)

    except AttributeError:

        for key, item in default_settings.iteritems():
            metric_name = item
            metric = swap_memory.__getattribute__(item)

            data = {
                'host': os.uname()[1],
                'service': 'swap_memory.{metric_name}'.format(metric_name=metric_name),
                'metric': metric,
                'state': determine_status('network_io.{metric_name}'.format(metric_name=metric_name), metric,
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('warn',default_settings['{metric_name}'.format(metric_name=metric_name)]['warn']),
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('crit',default_settings['{metric_name}'.format(metric_name=metric_name)]['crit']),
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('trigger', default_settings['{metric_name}'.format(metric_name=metric_name)]['trigger'])),
                'time': int(time.time()),
                'tags': settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('tags', []) + default_settings['{metric_name}'.format(metric_name=metric_name)]['tags']
            }
            return_data.append(data)

    return return_data
