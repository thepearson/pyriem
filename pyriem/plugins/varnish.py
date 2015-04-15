try:
    import time
except ImportError:
    print "Requirement: 'time' module not found."

try:
    import os
except ImportError:
    print "Requirement: 'os' module not found."

try:
    from subprocess import check_output
except ImportError:
    print "Requirement: 'subprocess' module not found."

from .common import determine_status


DEFAULT_TAGS = ['varnish']


_settings = {
    'stats': {
        'client_conn': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'client_drop': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'client_req': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'cache_hit': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'cache_hitpass': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'cache_miss': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'backend_conn': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'backend_unhealthy': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'backend_busy': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'backend_fail': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'backend_reuse': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'backend_toolate': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'backend_recycle': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'backend_retry': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
    }
}


cached_data = {}


def stats(settings=None):
    global cached_data

    return_varnish_stats = []

    default_settings = _settings['stats']
    varnish_stats = check_output(['varnishstat', '-1', '-f', ','.join(default_settings.keys())])

    for stat in varnish_stats.split('\n')[:-1]:
        # Just get the first two values
        metric_name, metric = stat.split()[0], int(stat.split()[1])
        
        do_run = True
        if '{metric_name}'.format(metric_name=metric_name) not in cached_data:
            current_metric = 0
            do_run = False
        else:
            current_metric = (metric - cached_data['{metric_name}'.format(metric_name=metric_name)]) / float(settings.get('freq'))

        cached_data['{metric_name}'.format(metric_name=metric_name)] = metric

        data = {
            'host': os.uname()[1],
            'service': 'varnish.stats.{metric_name}'.format(metric_name=metric_name),
            'metric': current_metric,
            'state': determine_status('network_io.{metric_name}'.format(metric_name=metric_name), current_metric,
                                      settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('warn',default_settings['{metric_name}'.format(metric_name=metric_name)]['warn']),
                                      settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('crit',default_settings['{metric_name}'.format(metric_name=metric_name)]['crit']),
                                      settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('trigger', default_settings['{metric_name}'.format(metric_name=metric_name)]['trigger'])),
            'time': int(time.time()),
            'tags': settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('tags', []) + default_settings['{metric_name}'.format(metric_name=metric_name)]['tags']
        }

        if do_run:
            return_varnish_stats.append(data)

    return return_varnish_stats
