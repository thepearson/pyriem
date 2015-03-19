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

BYTES_SENT_WARN = None
BYTES_RECV_WARN = None
PACKETS_SENT_WARN = None
PACKETS_RECV_WARN = None
ERRIN_WARN_WARN = None
ERROUT_WARN = None
DROPIN_WARN = None
DROPOUT_WARN = None

BYTES_SENT_CRIT = None
BYTES_RECV_CRIT = None
PACKETS_SENT_CRIT = None
PACKETS_RECV_CRIT = None
ERRIN_WARN_CRIT = None
ERROUT_CRIT = None
DROPIN_CRIT = None
DROPOUT_CRIT = None

BYTES_SENT_TRIGGER = None
BYTES_RECV_TRIGGER = None
PACKETS_SENT_TRIGGER = None
PACKETS_RECV_TRIGGER = None
ERRIN_WARN_TRIGGER = None
ERROUT_TRIGGER = None
DROPIN_TRIGGER = None
DROPOUT_TRIGGER = None


def parse_settings_network_io(settings):
    _settings = {
        'bytes_sent': {},
        'bytes_recv': {},
        'packets_sent': {},
        'packets_recv': {},
        'errin': {},
        'errout': {},
        'dropin': {},
        'dropout': {},
        'freq': settings['freq'] if 'freq' in settings else FREQ
    }

    # Triggers
    _settings['bytes_sent']['trigger'] = settings['bytes_sent']['trigger'] \
        if 'bytes_sent' in settings and 'trigger' in settings['bytes_sent'] else BYTES_SENT_TRIGGER

    _settings['bytes_recv']['trigger'] = settings['bytes_recv']['trigger'] \
        if 'bytes_recv' in settings and 'trigger' in settings['bytes_recv'] else BYTES_RECV_TRIGGER

    _settings['packets_sent']['trigger'] = settings['packets_sent']['trigger'] \
        if 'packets_sent' in settings and 'trigger' in settings['packets_sent'] else PACKETS_SENT_TRIGGER

    _settings['packets_recv']['trigger'] = settings['packets_recv']['trigger'] \
        if 'packets_recv' in settings and 'trigger' in settings['packets_recv'] else PACKETS_RECV_TRIGGER

    _settings['errin']['trigger'] = settings['errin']['trigger'] \
        if 'errin' in settings and 'trigger' in settings['errin'] else ERRIN_WARN_TRIGGER

    _settings['errout']['trigger'] = settings['errout']['trigger'] \
        if 'errout' in settings and 'trigger' in settings['errout'] else ERROUT_TRIGGER

    _settings['dropin']['trigger'] = settings['dropin']['trigger'] \
        if 'dropin' in settings and 'trigger' in settings['dropin'] else DROPIN_TRIGGER

    _settings['dropout']['trigger'] = settings['dropout']['trigger'] \
        if 'dropout' in settings and 'trigger' in settings['dropout'] else DROPOUT_TRIGGER

    # Warning Threshold
    _settings['bytes_sent']['warn'] = settings['bytes_sent']['warn'] \
        if 'bytes_sent' in settings and 'warn' in settings['bytes_sent'] else BYTES_SENT_WARN

    _settings['bytes_recv']['warn'] = settings['bytes_recv']['warn'] \
        if 'bytes_recv' in settings and 'warn' in settings['bytes_recv'] else BYTES_RECV_WARN

    _settings['packets_sent']['warn'] = settings['packets_sent']['warn'] \
        if 'packets_sent' in settings and 'warn' in settings['packets_sent'] else PACKETS_SENT_WARN

    _settings['packets_recv']['warn'] = settings['packets_recv']['warn'] \
        if 'packets_recv' in settings and 'warn' in settings['packets_recv'] else PACKETS_RECV_WARN

    _settings['errin']['warn'] = settings['errin']['warn'] \
        if 'errin' in settings and 'warn' in settings['errin'] else ERRIN_WARN_WARN

    _settings['errout']['warn'] = settings['errout']['warn'] \
        if 'errout' in settings and 'warn' in settings['errout'] else ERROUT_WARN

    _settings['dropin']['warn'] = settings['dropin']['warn'] \
        if 'dropin' in settings and 'warn' in settings['dropin'] else DROPIN_WARN

    _settings['dropout']['warn'] = settings['dropout']['warn'] \
        if 'dropout' in settings and 'warn' in settings['dropout'] else DROPOUT_WARN

    # Critical threshold
    _settings['bytes_sent']['crit'] = settings['bytes_sent']['crit'] \
        if 'bytes_sent' in settings and 'crit' in settings['bytes_sent'] else BYTES_SENT_CRIT

    _settings['bytes_recv']['crit'] = settings['bytes_recv']['crit'] \
        if 'bytes_recv' in settings and 'crit' in settings['bytes_recv'] else BYTES_RECV_CRIT

    _settings['packets_sent']['crit'] = settings['packets_sent']['crit'] \
        if 'packets_sent' in settings and 'crit' in settings['packets_sent'] else PACKETS_SENT_CRIT

    _settings['packets_recv']['crit'] = settings['packets_recv']['crit'] \
        if 'packets_recv' in settings and 'crit' in settings['packets_recv'] else PACKETS_RECV_CRIT

    _settings['errin']['crit'] = settings['errin']['crit'] \
        if 'errin' in settings and 'crit' in settings['errin'] else ERRIN_WARN_CRIT

    _settings['errout']['crit'] = settings['errout']['crit'] \
        if 'errout' in settings and 'crit' in settings['errout'] else ERROUT_CRIT

    _settings['dropin']['crit'] = settings['dropin']['crit'] \
        if 'dropin' in settings and 'crit' in settings['dropin'] else DROPIN_CRIT

    _settings['dropout']['crit'] = settings['dropout']['crit'] \
        if 'dropout' in settings and 'crit' in settings['dropout'] else DROPOUT_CRIT

    # Tags
    _settings['bytes_sent']['tags'] = settings['bytes_sent']['tags'] + ['network'] \
        if 'bytes_sent' in settings and 'tags' in settings['bytes_sent'] else ['network']

    _settings['bytes_recv']['tags'] = settings['bytes_recv']['tags'] + ['network'] \
        if 'bytes_recv' in settings and 'tags' in settings['bytes_recv'] else ['network']

    _settings['packets_sent']['tags'] = settings['packets_sent']['tags'] + ['network'] \
        if 'packets_sent' in settings and 'tags' in settings['packets_sent'] else ['network']

    _settings['packets_recv']['tags'] = settings['packets_recv']['tags'] + ['network'] \
        if 'packets_recv' in settings and 'tags' in settings['packets_recv'] else ['network']

    _settings['errin']['tags'] = settings['errin']['tags'] + ['network'] \
        if 'errin' in settings and 'tags' in settings['errin'] else ['network']

    _settings['errout']['tags'] = settings['errout']['tags'] + ['network'] \
        if 'errout' in settings and 'tags' in settings['errout'] else ['network']

    _settings['dropin']['tags'] = settings['dropin']['tags'] + ['network'] \
        if 'dropin' in settings and 'tags' in settings['dropin'] else ['network']

    _settings['dropout']['tags'] = settings['dropout']['tags'] + ['network'] \
        if 'dropout' in settings and 'tags' in settings['dropout'] else ['network']

    return _settings


cached_data = {}

def network_io(settings=None):
    global cached_data

    device_info = []

    net_io = psutil.net_io_counters(pernic=True)

    for device, vals in net_io.iteritems():
        for type, metric in vals.__dict__.iteritems():

            if '{type}.{dev}'.format(type=type, dev=device) not in cached_data:
                current_metric = 0
            else:
                current_metric = (metric - cached_data['{type}.{dev}'.format(type=type, dev=device)]) / settings['freq']

            cached_data['{type}.{dev}'.format(type=type, dev=device)] = metric

            data = {
                'host': os.uname()[1],
                'service': 'network_io.{device}.{type}'.format(device=device, type=type),
                'metric': current_metric,
                'state': determine_status('disk_io.{type}'.format(type=type), metric,
                                              settings['{type}'.format(type=type)]['warn'],
                                              settings['{type}'.format(type=type)]['crit'],
                                              settings['{type}'.format(type=type)]['trigger']),
                'time': int(time.time()),
                'tags': settings['{type}'.format(type=type)]['tags']
            }


            device_info.append(data)

    return device_info
