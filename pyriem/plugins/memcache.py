try:
    import re
except ImportError:
    print "Requirement: 're' module not found."

try:
    import telnetlib
except ImportError:
    print "Requirement: 'telnetlib' module not found."

try:
    import sys
except ImportError:
    print "Requirement: 'sys' module not found."

try:
    import time
except ImportError:
    print "Requirement: 'time' module not found."

try:
    import os
except ImportError:
    print "Requirement: 'os' module not found."


from .common import determine_status


DEFAULT_TAGS = ['memcache']

_settings = {
    'stats': {
        'bytes': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'bytes_read': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'bytes_written': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'cmd_flush': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'cmd_get': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'cmd_set': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'connection_structures': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'curr_connections': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'conn_yields': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'curr_items': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'delete_hits': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'delete_misses': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'evictions': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'get_hits': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'get_misses': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'incr_hits': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'incr_misses': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'reclaimed': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'total_connections': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS},
        'total_items': {'warn': None,'crit': None,'trigger': None,'tags': DEFAULT_TAGS}
    }
}

class MemcachedStats:

    _client = None
    _key_regex = re.compile(ur'ITEM (.*) \[(.*); (.*)\]')
    _slab_regex = re.compile(ur'STAT items:(.*):number')
    _stat_regex = re.compile(ur"STAT (.*) (.*)\r")

    def __init__(self, host='localhost', port='11211'):
        self._host = host
        self._port = port

    @property
    def client(self):
        if self._client is None:
            self._client = telnetlib.Telnet(self._host, self._port)
        return self._client

    def command(self, cmd):
        ' Write a command to telnet and return the response '
        self.client.write("%s\n" % cmd)
        return self.client.read_until('END')

    def key_details(self, sort=True, limit=100):
        ' Return a list of tuples containing keys and details '
        cmd = 'stats cachedump %s %s'
        keys = [key for id in self.slab_ids()
            for key in self._key_regex.findall(self.command(cmd % (id, limit)))]
        if sort:
            return sorted(keys)
        else:
            return keys

    def keys(self, sort=True, limit=100):
        ' Return a list of keys in use '
        return [key[0] for key in self.key_details(sort=sort, limit=limit)]

    def slab_ids(self):
        ' Return a list of slab ids in use '
        return self._slab_regex.findall(self.command('stats items'))

    def stats(self):
        ' Return a dict containing memcached stats '
        return dict(self._stat_regex.findall(self.command('stats')))



def stats(settings=None):

    return_stats = []
    default_settings = _settings['stats']

    if not settings:
        settings = _settings['stats']

    try:
        mem = MemcachedStats()
        stats = mem.stats()
    except:
        return None

    for key,row in stats.iteritems():
        metric_name = key
        metric = row

        if metric_name in default_settings:

            data = {
                'host': os.uname()[1],
                'service': 'memcache.stats.{metric_name}'.format(metric_name=metric_name),
                'metric': float(metric),
                'state': determine_status('stats.{metric_name}'.format(metric_name=metric_name), metric,
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('warn', default_settings['{metric_name}'.format(metric_name=metric_name)]['warn']),
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('crit', default_settings['{metric_name}'.format(metric_name=metric_name)]['crit']),
                                          settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('trigger', default_settings['{metric_name}'.format(metric_name=metric_name)]['trigger'])),
                'time': int(time.time()),
                'tags': settings.get('{metric_name}'.format(metric_name=metric_name), {}).get('tags', []) + default_settings['{metric_name}'.format(metric_name=metric_name)]['tags']
            }

            return_stats.append(data)

    return return_stats