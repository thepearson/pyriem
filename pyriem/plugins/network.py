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
  'network_io': {
    'frequency': 5,
    'ttl': 120,
    'warn': 4194304,
    'crit': 8388608
  }
}

cached_data = {}


def network_io(settings=None):
  global cached_data

  if not settings:
    settings = default_settings['network_io']

  device_info = []
  net_io = psutil.net_io_counters(pernic=True)
  for nic, vals in net_io.iteritems():


    if '{nic}_in_bps'.format(nic=nic) not in cached_data:
      bytes_in_per_second = 0
    else:
      bytes_in_per_second = (vals.bytes_recv - cached_data['{nic}_in_bps'.format(nic=nic)])/settings['frequency']

    cached_data['{nic}_in_bps'.format(nic=nic)] = vals.bytes_recv

    if '{nic}_out_bps'.format(nic=nic) not in cached_data:
      bytes_out_per_second = 0
    else:
      bytes_out_per_second = (vals.bytes_sent - cached_data['{nic}_out_bps'.format(nic=nic)])/settings['frequency']

    cached_data['{nic}_out_bps'.format(nic=nic)] = vals.bytes_sent

    in_state = 'ok'
    if bytes_in_per_second >= settings['warn']:
      in_state = 'warning'

    if bytes_in_per_second >= settings['crit']:
      in_state = 'critical'

    out_state = 'ok'
    if bytes_out_per_second >= settings['warn']:
      out_state = 'warning'

    if bytes_out_per_second >= settings['crit']:
      out_state = 'critical'

    device_info.append({
      'host': os.uname()[1],
      'service': 'network_inbound_{device}'.format(device=nic),
      'metric': bytes_in_per_second,
      'state': in_state,
      'time': int(time.time()),
      'tags': [__name__],
      'ttl': settings['ttl']
      #'description': 'Disk status is "{state}". Total size is {total} and disk has {free} free.'.format(state=state, total=space.total, free=space.free)
    })

    device_info.append({
      'host': os.uname()[1],
      'service': 'network_outboud_{device}'.format(device=nic),
      'metric': bytes_out_per_second,
      'state': out_state,
      'time': int(time.time()),
      'tags': [__name__],
      'ttl': settings['ttl']
      #'description': 'Disk status is "{state}". Total size is {total} and disk has {free} free.'.format(state=state, total=space.total, free=space.free)
    })

  return device_info
