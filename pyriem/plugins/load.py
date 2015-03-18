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


FREQ = 5

# Based on a 1-2 CPU host
WARN_1_MIN = 2.0
WARN_5_MIN = 1.0
WARN_15_MIN = 0.8

CRIT_1_MIN = 4.0
CRIT_5_MIN = 2.0
CRIT_15_MIN = 1.2


def parse_settings_load_avg(settings):
    """
    Define the default config so that the yaml file doesn't have to define everything
    """
    _settings = {
        '1_min': {},
        '5_min': {},
        '15_min': {},
        'freq': settings['freq'] if 'freq' in settings else FREQ
    }

    # Warning threashold
    _settings['1_min']['warn'] = settings['1_min']['warn'] \
        if '1_min' in settings and 'warn' in settings['1_min'] else WARN_1_MIN

    _settings['5_min']['warn'] = settings['5_min']['warn'] \
        if '5_min' in settings and 'warn' in settings['5_min'] else WARN_5_MIN

    _settings['15_min']['warn'] = settings['15_min']['warn'] \
        if '15_min' in settings and 'warn' in settings['15_min'] else WARN_15_MIN

    # Critical threashold
    _settings['1_min']['crit'] = settings['1_min']['crit'] \
        if '1_min' in settings and 'crit' in settings['1_min'] else CRIT_1_MIN

    _settings['5_min']['crit'] = settings['5_min']['crit'] \
        if '5_min' in settings and 'crit' in settings['1_min'] else CRIT_5_MIN

    _settings['15_min']['crit'] = settings['15_min']['crit'] \
        if '15_min' in settings and 'crit' in settings['15_min'] else CRIT_15_MIN

    # Tags
    _settings['1_min']['tags'] = settings['1_min']['tags'] + ['load'] \
        if '1_min' in settings and 'tags' in settings['1_min'] else ['load']

    _settings['5_min']['tags'] = settings['5_min']['tags'] + ['load'] \
        if '5_min' in settings and 'tags' in settings['5_min'] else ['load']

    _settings['15_min']['tags'] = settings['15_min']['tags'] + ['load'] \
        if '15_min' in settings and 'tags' in settings['15_min'] else ['load']

    return _settings


def load_avg(settings):
    """
    Returns the load average
    """
    load = os.getloadavg()
    load_data = []

    data_1 = {
        'host': os.uname()[1],
        'service': 'load_avg.1_min',
        'metric': load[0],
        'state': determine_status('1_min', load[0], settings['1_min']['warn'], settings['1_min']['crit']),
        'time': int(time.time()),
        'tags': settings['1_min']['tags']
    }

    load_data.append(data_1)

    data_5 = {
        'host': os.uname()[1],
        'service': 'load_avg.5_min',
        'metric': load[1],
        'state': determine_status('5_min', load[1], settings['5_min']['warn'], settings['5_min']['crit']),
        'time': int(time.time()),
        'tags': settings['5_min']['tags'],
    }

    load_data.append(data_5)

    data_15 = {
        'host': os.uname()[1],
        'service': 'load_avg.15_min',
        'metric': load[2],
        'state': determine_status('15_min', load[2], settings['15_min']['warn'], settings['15_min']['crit']),
        'time': int(time.time()),
        'tags': settings['15_min']['tags']
    }

    load_data.append(data_15)

    return load_data