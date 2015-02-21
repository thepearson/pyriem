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
  'virtual_memory': {
    'frequency': 10,
    'warn': 0.95,
    'crit': 0.98
  },
  'swap_memory': {
    'frequency': 10,
    'warn': 0.15,
    'crit': 0.25
  }
}

def virtual_memory(settings=None):
  if not settings:
    settings = default_settings['virtual_memory']

  virtual_memory = psutil.virtual_memory()

  state = 'ok'
  if virtual_memory.percent >= (settings['warn'] * 100.):
    state = 'warning'

  if virtual_memory.percent >= (settings['crit'] * 100.):
    state = 'critical'

  return_data = []
  for item in virtual_memory.__dict__.iteritems():
    type = item[0]
    metric = item[1]

    data = {
      'host': os.uname()[1],
      'service': 'virtual_memory_{type}'.format(type=type),
      'metric': metric,
      'state': state,
      'time': int(time.time()),
      'tags': [__name__],
      'description': 'Virtual memory metric "{metric}" which is in "{state}" state'.format(metric=type, state=state)
    }

    if 'ttl' in settings:
      data['ttl'] = settings['ttl']

    return_data.append(data)

  return return_data



def swap_memory(settings=None):
  if not settings:
    settings = default_settings['swap_memory']

  swap_memory = psutil.swap_memory()

  state = 'ok'
  if swap_memory.percent >= (settings['warn'] * 100.):
    state = 'warning'

  if swap_memory.percent >= (settings['crit'] * 100.):
    state = 'critical'

  return_data = []
  for item in swap_memory.__dict__.iteritems():
    type = item[0]
    metric = item[1]

    data = {
      'host': os.uname()[1],
      'service': 'swap_memory_{type}'.format(type=type),
      'metric': metric,
      'state': state,
      'time': int(time.time()),
      'tags': [__name__],
      'description': 'Swap memory metric "{metric}" which is in "{state}" state'.format(metric=type, state=state)
    }

    if 'ttl' in settings:
      data['ttl'] = settings['ttl']

    return_data.append(data)

  return return_data
