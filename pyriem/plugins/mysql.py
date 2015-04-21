try:
    import time
except ImportError:
    print "Requirement: 'time' module not found."

try:
    import MySQLdb
except ImportError:
    print "Requirement: 'os' module not found."

try:
    import os
except ImportError:
    print "Requirement: 'os' module not found."

from .common import determine_status


DEFAULT_TAGS = ['mysql']

_settings = {
    'connection': {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'db': 'mysql'
    },
    'status': {
        'freq': 5,

        'Connections': {'persec': True, 'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},

        'Qcache_free_blocks': {'persec': False, 'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'Qcache_free_memory': {'persec': False, 'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'Qcache_hits': {'persec': True, 'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'Qcache_inserts': {'persec': True, 'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'Qcache_lowmem_prunes': {'persec': True, 'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'Qcache_not_cached': {'persec': True, 'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'Qcache_queries_in_cache': {'persec': False, 'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'Qcache_total_blocks': {'persec': False, 'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},

        'Queries': {'persec': True, 'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
    }
}


cached_data = {}


def status(settings=None):
    global cached_data

    default_settings = _settings['status']

    data_rows = []
    db = MySQLdb.connect(host=settings.get('connection', {}).get('host', 'localhost'),
                         user=settings.get('connection', {}).get('user', 'root'),
                         passwd=settings.get('connection', {}).get('password', ''))
    cur = db.cursor()
    cur.execute("SHOW STATUS")

    for row in cur.fetchall():
        metric_name = row[0]

        if metric_name in _settings['status']:

            metric = int(row[1])

            do_run = True

            if _settings['status'][metric_name]['persec'] is True:
                if '{metric_name}'.format(metric_name=metric_name) not in cached_data:
                    current_metric = 0
                    do_run = False
                else:
                    current_metric = (metric - cached_data['{metric_name}'.format(metric_name=metric_name)]) / float(settings.get('freq'))

                cached_data['{metric_name}'.format(metric_name=metric_name)] = metric
            else:
                current_metric = metric

            data = {
                'host': os.uname()[1],
                'service': 'mysql.status.{metric_name}'.format(metric_name=metric_name),
                'metric': current_metric,
                'state': determine_status('network_io.{metric_name}'.format(metric_name=metric_name), current_metric,
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('warn',default_settings['{metric_name}'.format(metric_name=metric_name)]['warn']),
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('crit',default_settings['{metric_name}'.format(metric_name=metric_name)]['crit']),
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('trigger', default_settings['{metric_name}'.format(metric_name=metric_name)]['trigger'])),
                'time': int(time.time()),
                'tags': settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('tags', []) + default_settings['{metric_name}'.format(metric_name=metric_name)]['tags']
            }

            if do_run:
                data_rows.append(data)

    return data_rows
