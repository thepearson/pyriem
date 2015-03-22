try:
    import time
except ImportError:
    print "Requirement: 'time' module not found."

try:
    import os
except ImportError:
    print "Requirement: 'os' module not found."

try:
    import psutil
except ImportError:
    print "Module 'psutil' required"

from .common import determine_status


DEFAULT_TAGS = ['load']

_settings = {
    'load_avg': {
        'freq': 5,
        '1_min': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        '5_min': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        '15_min': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
    }
}


def load_avg(settings):
    """
    Returns the load average
    """
    default_settings = _settings['load_avg']

    load = os.getloadavg()
    load_data = []

    data_1 = {
        'host': os.uname()[1],
        'service': 'load_avg.1_min',
        'metric': load[0],
        'state': determine_status('load_avg.1_min', load[0],
                                          settings.get('1_min', {}).get('warn', default_settings['1_min']['warn']),
                                          settings.get('1_min', {}).get('crit', default_settings['1_min']['crit']),
                                          settings.get('1_min', {}).get('trigger', default_settings['1_min']['trigger'])),
        'time': int(time.time()),
        'tags': settings.get('1_min', {}).get('tags', []) + default_settings['1_min']['tags']
    }

    load_data.append(data_1)

    data_5 = {
        'host': os.uname()[1],
        'service': 'load_avg.5_min',
        'metric': load[1],
        'state': determine_status('load_avg.5_min', load[1],
                                          settings.get('5_min', {}).get('warn', default_settings['5_min']['warn']),
                                          settings.get('5_min', {}).get('crit', default_settings['5_min']['crit']),
                                          settings.get('5_min', {}).get('trigger', default_settings['5_min']['trigger'])),
        'time': int(time.time()),
        'tags': settings.get('5_min', {}).get('tags', []) + default_settings['5_min']['tags']
    }

    load_data.append(data_5)

    data_15 = {
        'host': os.uname()[1],
        'service': 'load_avg.15_min',
        'metric': load[2],
        'state': determine_status('load_avg.15_min', load[2],
                                          settings.get('15_min', {}).get('warn', default_settings['15_min']['warn']),
                                          settings.get('15_min', {}).get('crit', default_settings['15_min']['crit']),
                                          settings.get('15_min', {}).get('trigger', default_settings['15_min']['trigger'])),
        'time': int(time.time()),
        'tags': settings.get('15_min', {}).get('tags', []) + default_settings['15_min']['tags']
    }

    load_data.append(data_15)

    return load_data