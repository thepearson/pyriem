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

VIRT_TOTAL_WARN = None
VIRT_AVAILABLE_WARN = None
VIRT_PERCENT_WARN = 90.0
VIRT_USED_WARN = None
VIRT_FREE_WARN = None
VIRT_ACTIVE_WARN = None
VIRT_INACTIVE_WARN = None
VIRT_BUFFERS_WARN = None
VIRT_CACHED_WARN = None

VIRT_TOTAL_CRIT = None
VIRT_AVAILABLE_CRIT = None
VIRT_PERCENT_CRIT = 95.0
VIRT_USED_CRIT = None
VIRT_FREE_CRIT = None
VIRT_ACTIVE_CRIT = None
VIRT_INACTIVE_CRIT = None
VIRT_BUFFERS_CRIT = None
VIRT_CACHED_CRIT = None

VIRT_TOTAL_TRIGGER = 'ignore'
VIRT_AVAILABLE_TRIGGER = None
VIRT_AVAILABLE_TRIGGER = None
VIRT_PERCENT_TRIGGER = None
VIRT_USED_TRIGGER = None
VIRT_FREE_TRIGGER = None
VIRT_ACTIVE_TRIGGER = None
VIRT_INACTIVE_TRIGGER = None
VIRT_BUFFERS_TRIGGER = None
VIRT_CACHED_TRIGGER = None


SWAP_TOTAL_WARN = None
SWAP_PERCENT_WARN = 25.0
SWAP_USED_WARN = None
SWAP_FREE_WARN = None
SWAP_SIN_WARN = None
SWAP_SOUT_WARN = None

SWAP_TOTAL_CRIT = None
SWAP_PERCENT_CRIT = 50.0
SWAP_USED_CRIT = None
SWAP_FREE_CRIT = None
SWAP_SIN_CRIT = None
SWAP_SOUT_CRIT = None

SWAP_TOTAL_TRIGGER = None
SWAP_PERCENT_TRIGGER = None
SWAP_USED_TRIGGER = None
SWAP_FREE_TRIGGER = None
SWAP_SIN_TRIGGER = None
SWAP_SOUT_TRIGGER = None


def parse_settings_virtual_memory(settings):
    """
    Define the default config so that the yaml file doesn't have to define everything
    """
    _settings = {}

    # All possible metrics
    _settings['freq'] = settings['freq'] if 'freq' in settings else FREQ
    _settings['total'] = {}
    _settings['available'] = {}
    _settings['percent'] = {}
    _settings['used'] = {}
    _settings['free'] = {}
    _settings['active'] = {}
    _settings['inactive'] = {}
    _settings['buffers'] = {}
    _settings['cached'] = {}

    # Trigger
    _settings['total']['trigger'] = settings['total']['trigger'] \
        if 'total' in settings and 'trigger' in settings['total'] else VIRT_TOTAL_TRIGGER

    _settings['available']['trigger'] = settings['available']['trigger'] \
        if 'available' in settings and 'trigger' in settings['available'] else VIRT_AVAILABLE_TRIGGER

    _settings['percent']['trigger'] = settings['percent']['trigger'] \
        if 'percent' in settings and 'trigger' in settings['percent'] else VIRT_PERCENT_TRIGGER

    _settings['used']['trigger'] = settings['used']['trigger'] \
        if 'used' in settings and 'trigger' in settings['used'] else VIRT_USED_TRIGGER

    _settings['free']['trigger'] = settings['free']['trigger'] \
        if 'free' in settings and 'trigger' in settings['free'] else VIRT_FREE_TRIGGER

    _settings['active']['trigger'] = settings['active']['trigger'] \
        if 'active' in settings and 'trigger' in settings['active'] else VIRT_ACTIVE_TRIGGER

    _settings['inactive']['trigger'] = settings['inactive']['trigger'] \
        if 'inactive' in settings and 'trigger' in settings['inactive'] else VIRT_INACTIVE_TRIGGER

    _settings['buffers']['trigger'] = settings['buffers']['trigger'] \
        if 'buffers' in settings and 'trigger' in settings['buffers'] else VIRT_BUFFERS_TRIGGER

    _settings['cached']['trigger'] = settings['cached']['trigger'] \
        if 'cached' in settings and 'trigger' in settings['cached'] else VIRT_CACHED_TRIGGER

    # Warning threshold
    _settings['total']['warn'] = settings['total']['warn'] \
        if 'total' in settings and 'warn' in settings['total'] else VIRT_TOTAL_WARN

    _settings['available']['warn'] = settings['available']['warn'] \
        if 'available' in settings and 'warn' in settings['available'] else VIRT_AVAILABLE_WARN

    _settings['percent']['warn'] = settings['percent']['warn'] \
        if 'percent' in settings and 'warn' in settings['percent'] else VIRT_PERCENT_WARN

    _settings['used']['warn'] = settings['used']['warn'] \
        if 'used' in settings and 'warn' in settings['used'] else VIRT_USED_WARN

    _settings['free']['warn'] = settings['free']['warn'] \
        if 'free' in settings and 'warn' in settings['free'] else VIRT_FREE_WARN

    _settings['active']['warn'] = settings['active']['warn'] \
        if 'active' in settings and 'warn' in settings['active'] else VIRT_ACTIVE_WARN

    _settings['inactive']['warn'] = settings['inactive']['warn'] \
        if 'inactive' in settings and 'warn' in settings['inactive'] else VIRT_INACTIVE_WARN

    _settings['buffers']['warn'] = settings['buffers']['warn'] \
        if 'buffers' in settings and 'warn' in settings['buffers'] else VIRT_BUFFERS_WARN

    _settings['cached']['warn'] = settings['cached']['warn'] \
        if 'cached' in settings and 'warn' in settings['cached'] else VIRT_CACHED_WARN

    # Critical threshold
    _settings['total']['crit'] = settings['total']['crit'] \
        if 'total' in settings and 'crit' in settings['total'] else VIRT_TOTAL_CRIT

    _settings['available']['crit'] = settings['available']['crit'] \
        if 'available' in settings and 'crit' in settings['available'] else VIRT_AVAILABLE_CRIT

    _settings['percent']['crit'] = settings['percent']['crit'] \
        if 'percent' in settings and 'crit' in settings['percent'] else VIRT_PERCENT_CRIT

    _settings['used']['crit'] = settings['used']['crit'] \
        if 'used' in settings and 'crit' in settings['used'] else VIRT_USED_CRIT

    _settings['free']['crit'] = settings['free']['crit'] \
        if 'free' in settings and 'crit' in settings['free'] else VIRT_FREE_CRIT

    _settings['active']['crit'] = settings['active']['crit'] \
        if 'active' in settings and 'crit' in settings['active'] else VIRT_ACTIVE_CRIT

    _settings['inactive']['crit'] = settings['inactive']['crit'] \
        if 'inactive' in settings and 'crit' in settings['inactive'] else VIRT_INACTIVE_CRIT

    _settings['buffers']['crit'] = settings['buffers']['crit'] \
        if 'buffers' in settings and 'crit' in settings['buffers'] else VIRT_BUFFERS_CRIT

    _settings['cached']['crit'] = settings['cached']['crit'] \
        if 'cached' in settings and 'crit' in settings['cached'] else VIRT_CACHED_CRIT

    # Tags
    _settings['total']['tags'] = settings['total']['tags'] + ['memory'] \
        if 'total' in settings and 'tags' in settings['total'] else ['memory']

    _settings['available']['tags'] = settings['available']['tags'] + ['memory'] \
        if 'available' in settings and 'tags' in settings['available'] else ['memory']

    _settings['percent']['tags'] = settings['percent']['tags'] + ['memory'] \
        if 'percent' in settings and 'tags' in settings['percent'] else ['memory']

    _settings['used']['tags'] = settings['used']['tags'] + ['memory'] \
        if 'used' in settings and 'tags' in settings['used'] else ['memory']

    _settings['free']['tags'] = settings['free']['tags'] + ['memory'] \
        if 'free' in settings and 'tags' in settings['free'] else ['memory']

    _settings['active']['tags'] = settings['active']['tags'] + ['memory'] \
        if 'active' in settings and 'tags' in settings['active'] else ['memory']

    _settings['inactive']['tags'] = settings['inactive']['tags'] + ['memory'] \
        if 'inactive' in settings and 'tags' in settings['inactive'] else ['memory']

    _settings['buffers']['tags'] = settings['buffers']['tags'] + ['memory'] \
        if 'buffers' in settings and 'tags' in settings['buffers'] else ['memory']

    _settings['cached']['tags'] = settings['cached']['tags'] + ['memory'] \
        if 'cached' in settings and 'tags' in settings['cached'] else ['memory']

    return _settings


def parse_settings_swap_memory(settings):
    _settings = {}

    # All possible metrics
    _settings['freq'] = settings['freq'] if 'freq' in settings else FREQ
    _settings['total'] = {}
    _settings['percent'] = {}
    _settings['used'] = {}
    _settings['free'] = {}
    _settings['sin'] = {}
    _settings['sout'] = {}

    # Trigger
    _settings['total']['trigger'] = settings['total']['trigger'] \
        if 'total' in settings and 'trigger' in settings['total'] else SWAP_TOTAL_TRIGGER

    _settings['percent']['trigger'] = settings['percent']['trigger'] \
        if 'percent' in settings and 'trigger' in settings['percent'] else SWAP_PERCENT_TRIGGER

    _settings['used']['trigger'] = settings['used']['trigger'] \
        if 'used' in settings and 'trigger' in settings['used'] else SWAP_USED_TRIGGER

    _settings['free']['trigger'] = settings['free']['trigger'] \
        if 'free' in settings and 'trigger' in settings['free'] else SWAP_FREE_TRIGGER

    _settings['sin']['trigger'] = settings['sin']['trigger'] \
        if 'sin' in settings and 'trigger' in settings['sin'] else SWAP_SIN_TRIGGER

    _settings['sout']['trigger'] = settings['sout']['trigger'] \
        if 'sout' in settings and 'trigger' in settings['sout'] else SWAP_SOUT_TRIGGER

    # Warning threshold
    _settings['total']['warn'] = settings['total']['warn'] \
        if 'total' in settings and 'warn' in settings['total'] else SWAP_TOTAL_WARN

    _settings['percent']['warn'] = settings['percent']['warn'] \
        if 'percent' in settings and 'warn' in settings['percent'] else SWAP_PERCENT_WARN

    _settings['used']['warn'] = settings['used']['warn'] \
        if 'used' in settings and 'warn' in settings['used'] else SWAP_USED_WARN

    _settings['free']['warn'] = settings['free']['warn'] \
        if 'free' in settings and 'warn' in settings['free'] else SWAP_FREE_WARN

    _settings['sin']['warn'] = settings['sin']['warn'] \
        if 'sin' in settings and 'warn' in settings['sin'] else SWAP_SIN_WARN

    _settings['sout']['warn'] = settings['sout']['warn'] \
        if 'sout' in settings and 'warn' in settings['sout'] else SWAP_SOUT_WARN

    # Critical threshold
    _settings['total']['crit'] = settings['total']['crit'] \
        if 'total' in settings and 'crit' in settings['total'] else SWAP_TOTAL_CRIT

    _settings['percent']['crit'] = settings['percent']['crit'] \
        if 'percent' in settings and 'crit' in settings['percent'] else SWAP_PERCENT_CRIT

    _settings['used']['crit'] = settings['used']['crit'] \
        if 'used' in settings and 'crit' in settings['used'] else SWAP_USED_CRIT

    _settings['free']['crit'] = settings['free']['crit'] \
        if 'free' in settings and 'crit' in settings['free'] else SWAP_FREE_CRIT

    _settings['sin']['crit'] = settings['sin']['crit'] \
        if 'sin' in settings and 'crit' in settings['sin'] else SWAP_SIN_CRIT

    _settings['sout']['crit'] = settings['sout']['crit'] \
        if 'sout' in settings and 'crit' in settings['sout'] else SWAP_SOUT_CRIT

    # Tags
    _settings['total']['tags'] = settings['total']['tags'] + ['memory'] \
        if 'total' in settings and 'tags' in settings['total'] else ['memory']

    _settings['percent']['tags'] = settings['percent']['tags'] + ['memory'] \
        if 'percent' in settings and 'tags' in settings['percent'] else ['memory']

    _settings['used']['tags'] = settings['used']['tags'] + ['memory'] \
        if 'used' in settings and 'tags' in settings['used'] else ['memory']

    _settings['free']['tags'] = settings['free']['tags'] + ['memory'] \
        if 'free' in settings and 'tags' in settings['free'] else ['memory']

    _settings['sin']['tags'] = settings['sin']['tags'] + ['memory'] \
        if 'sin' in settings and 'tags' in settings['sin'] else ['memory']

    _settings['sout']['tags'] = settings['sout']['tags'] + ['memory'] \
        if 'sout' in settings and 'tags' in settings['sout'] else ['memory']

    return _settings


def virtual_memory(settings):
    """
    Virtual memory collector
    """

    virtual_memory = psutil.virtual_memory()

    return_data = []

    try:
        for item in virtual_memory.__dict__.iteritems():
            type = item[0]
            metric = item[1]

            data = {
                'host': os.uname()[1],
                'service': 'virtual_memory.{type}'.format(type=type),
                'metric': metric,
                'state': determine_status('virtual_memory.{type}'.format(type=type), metric,
                                          settings['{type}'.format(type=type)]['warn'],
                                          settings['{type}'.format(type=type)]['crit'],
                                          settings['{type}'.format(type=type)]['trigger']),
                'time': int(time.time()),
                'tags': settings['{type}'.format(type=type)]['tags']
            }
            return_data.append(data)

    except AttributeError:

        for item in ['total', 'available', 'percent', 'used', 'free', 'active', 'inactive', 'buffers', 'cached']:

            type = item
            metric = virtual_memory.__getattribute__(item)

            data = {
                'host': os.uname()[1],
                'service': 'virtual_memory.{type}'.format(type=type),
                'metric': metric,
                'state': determine_status('virtual_memory.{type}'.format(type=type), metric,
                                          settings['{type}'.format(type=type)]['warn'],
                                          settings['{type}'.format(type=type)]['crit'],
                                          settings['{type}'.format(type=type)]['trigger']),
                'time': int(time.time()),
                'tags': settings['{type}'.format(type=type)]['tags']
            }

            if 'ttl' in settings:
                data['ttl'] = settings['ttl']

            return_data.append(data)

    return return_data


def swap_memory(settings):
    swap_memory = psutil.swap_memory()

    return_data = []

    try:
        for item in swap_memory.__dict__.iteritems():
            type = item[0]
            metric = item[1]

            data = {
                'host': os.uname()[1],
                'service': 'swap_memory.{type}'.format(type=type),
                'metric': metric,
                'state': determine_status('swap_memory.{type}'.format(type=type), metric,
                                          settings['{type}'.format(type=type)]['warn'],
                                          settings['{type}'.format(type=type)]['crit'],
                                          settings['{type}'.format(type=type)]['trigger']),
                'time': int(time.time()),
                'tags': settings['{type}'.format(type=type)]['tags']
            }

            return_data.append(data)

    except AttributeError:

        for item in ['total', 'used', 'free', 'percent', 'sin', 'sout']:
            type = item
            metric = swap_memory.__getattribute__(item)

            data = {
                'host': os.uname()[1],
                'service': 'swap_memory.{type}'.format(type=type),
                'metric': metric,
                'state': determine_status('swap_memory.{type}'.format(type=type), metric,
                                          settings['{type}'.format(type=type)]['warn'],
                                          settings['{type}'.format(type=type)]['crit'],
                                          settings['{type}'.format(type=type)]['trigger']),
                'time': int(time.time()),
                'tags': settings['{type}'.format(type=type)]['tags']
            }
            return_data.append(data)

    return return_data
