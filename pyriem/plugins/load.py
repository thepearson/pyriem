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


"""
Percentage modifiers of total CPU's
for example if there was 1 CPU then a modifier of 1.5 would indicate a load of 1.5. If there was
2 CPU's then a modifier of 1.5 would mean a load of 3.0, 3 CPU's a load of 4.5 etc.

Format is [warning, critical] - this can be overridden in the config file with the following format

"""
default_settings = {
  'one_minute': {
    'frequency': 5,
    'warn': 2.0,
    'crit': 4.0
  },
  'five_minute': {
    'frequency': 10,
    'warn': 1.0,
    'crit': 2.0
  },
  'fifteen_minute': {
    'frequency': 15,
    'warn': 0.8,
    'crit': 1.2
  }
}

def _get_cpus():
  try:
    return psutil.cpu_count()
  except AttributeError:
    return psutil.NUM_CPUS


def one_minute(settings=None):
  """ Returns the 1 minute load average
  """
  load = os.getloadavg()

  if not settings:
    settings = default_settings['one_minute']

  cpus = float(_get_cpus())
  load_as_percentage = load[0]/cpus

  state = 'ok'
  if load_as_percentage >= settings['warn']:
    state = 'warning'
  if load_as_percentage >= settings['crit']:
    state = 'critical'

  data = {
    'host': os.uname()[1],
    'service': 'load_1_minute',
    'metric': load[0],
    'state': state,
    'time': int(time.time()),
    'tags': [__name__],
    'description': 'One minute load average in "{state}" state'.format(state=state)
  }

  if 'ttl' in settings:
    data['ttl'] = settings['ttl']

  return data


def five_minute(settings=None):
  """ Returns the 5 minute load average
  """
  load = os.getloadavg()

  if not settings:
    settings = default_settings['five_minute']

  cpus = float(_get_cpus())
  load_as_percentage = load[1]/cpus

  state = 'ok'
  if load_as_percentage >= settings['warn']:
    state = 'warning'
  if load_as_percentage >= settings['crit']:
    state = 'critical'

  data = {
    'host': os.uname()[1],
    'service': 'load_5_minute',
    'metric': load[1],
    'state': state,
    'time': int(time.time()),
    'tags': [__name__],
    'description': 'Five minute load average in "{state}" state'.format(state=state)
  }

  if 'ttl' in settings:
    data['ttl'] = settings['ttl']

  return data


def fifteen_minute(settings=None):
  """ Returns the 15 minute load average
  """
  load = os.getloadavg()

  if not settings:
    settings = default_settings['fifteen_minute']

  cpus = float(_get_cpus())
  load_as_percentage = load[2]/cpus

  state = 'ok'
  if load_as_percentage >= settings['warn']:
    state = 'warning'
  if load_as_percentage >= settings['crit']:
    state = 'critical'

  data = {
    'host': os.uname()[1],
    'service': 'load_15_minute',
    'metric': load[2],
    'state': state,
    'time': int(time.time()),
    'tags': [__name__],
    'description': 'Fifteen minute load average in "{state}" state'.format(state=state)
  }

  if 'ttl' in settings:
    data['ttl'] = settings['ttl']

  return data
