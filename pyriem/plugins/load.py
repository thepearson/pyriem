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


FREQ = 5

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
  _settings = {}

  # All possible metrics
  _settings['freq'] = settings['freq'] if 'freq' in settings else FREQ
  _settings['1_min'] = {}
  _settings['5_min'] = {}
  _settings['15_min'] = {}

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



def _get_cpus():
  """
  Returns a count of CPU's for this host
  """
  try:
    return psutil.cpu_count()
  except AttributeError:
    return psutil.NUM_CPUS


def load_avg(settings):
  """
  Returns the load average
  """


  load = os.getloadavg()
  cpus = float(_get_cpus())
  load_data = []


  # 1 minute load average
  load_as_percentage = load[0]/cpus

  state = 'ok'
  if load_as_percentage >= settings['1_min']['warn']:
    state = 'warning'
  if load_as_percentage >= settings['1_min']['crit']:
    state = 'critical'

  data_1 = {
    'host': os.uname()[1],
    'service': 'load_avg.1_min',
    'metric': load[0],
    'state': state,
    'time': int(time.time()),
    'tags': settings['1_min']['tags']
  }

  load_data.append(data_1)



  # 5 minute load average
  load_as_percentage = load[1]/cpus

  state = 'ok'
  if load_as_percentage >= settings['5_min']['warn']:
    state = 'warning'
  if load_as_percentage >= settings['5_min']['crit']:
    state = 'critical'

  data_5 = {
    'host': os.uname()[1],
    'service': 'load_avg.5_min',
    'metric': load[1],
    'state': state,
    'time': int(time.time()),
    'tags': settings['5_min']['tags'],
  }

  load_data.append(data_5)



  # 15 minute load average
  load_as_percentage = load[2]/cpus

  state = 'ok'
  if load_as_percentage >= settings['15_min']['warn']:
    state = 'warning'
  if load_as_percentage >= settings['15_min']['crit']:
    state = 'critical'

  data_15 = {
    'host': os.uname()[1],
    'service': 'load_avg.15_min',
    'metric': load[2],
    'state': state,
    'time': int(time.time()),
    'tags': settings['15_min']['tags']
  }

  load_data.append(data_15)

  return load_data