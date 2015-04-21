try:
    import time
except ImportError:
    print "Requirement: 'time' module not found."

try:
    import os
except ImportError:
    print "Requirement: 'os' module not found."

try:
    import urllib2
except ImportError:
    print "Requirement: 'os' module not found."


from .common import determine_status


DEFAULT_TAGS = ['apache2']

_settings = {
    'url': 'http://localhost/server-status?auto',
    'status': {
        'Uptime': {'persec': False, 'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'IdleWorkers': {'persec': False, 'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'TotalAccesses': {'persec': False, 'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'TotalkBytes': {'persec': False, 'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'BytesPerReq': {'persec': False, 'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'CPULoad': {'persec': False, 'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'BytesPerSec': {'persec': False, 'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'ReqPerSec': {'persec': False, 'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'BusyWorkers': {'persec': False, 'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS}
    }
}


def _get_status(url):
    return_val = {}
    response = urllib2.urlopen(url)
    string = response.read()
    for line in string.split("\n"):
        if len(line.strip()) > 0:
            var, val = line.strip().split(": ")[0].replace(" ", ""), line.strip().split(": ")[1]
            return_val[var] = val
    return return_val


def status(settings=None):

    return_apache_stats = []
    default_settings = _settings['status']
    apache_status = _get_status(_settings['url'])

    for key,row in apache_status.iteritems():
        metric_name = key
        metric = row

        if metric_name in default_settings:

            data = {
                'host': os.uname()[1],
                'service': 'apache2.status.{metric_name}'.format(metric_name=metric_name),
                'metric': float(metric),
                'state': determine_status('status.{metric_name}'.format(metric_name=metric_name), metric,
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('warn', default_settings['{metric_name}'.format(metric_name=metric_name)]['warn']),
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('crit', default_settings['{metric_name}'.format(metric_name=metric_name)]['crit']),
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('trigger', default_settings['{metric_name}'.format(metric_name=metric_name)]['trigger'])),
                'time': int(time.time()),
                'tags': settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('tags', []) + default_settings['{metric_name}'.format(metric_name=metric_name)]['tags']
            }

            return_apache_stats.append(data)

    return return_apache_stats
