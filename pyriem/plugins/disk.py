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


default_settings = {
  'disk_usage': {
    'frequency': 3600,
    'warn': 0.8,
    'crit': 0.9
  }
}


def disk_usage(settings=None):
  """ Return statistics on mounted system disks
  """
  if not settings:
    settings = default_settings['disk_usage']

  disk_info = []
  disks = psutil.disk_partitions()

  for disk in disks:

    space = psutil.disk_usage(disk.mountpoint)
    percentage = (space.percent / 100.)

    state = 'ok'
    if percentage >= settings['warn']:
      state = 'warning'

    if percentage >= settings['crit']:
      state = 'critical'

    data = {
      'host': os.uname()[1],
      'service': 'disk_usage_{device}'.format(device=disk.device.split('/')[-1:][0]),
      'metric': percentage,
      'state': state,
      'time': int(time.time()),
      'tags': [__name__],
      'description': 'Disk status is "{state}". Total size is {total} and disk has {free} free.'.format(state=state, total=space.total, free=space.free)
    }

    if 'ttl' in settings:
      data['ttl'] = settings['ttl']

    disk_info.append(data)

  return disk_info
