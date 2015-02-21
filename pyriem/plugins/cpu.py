try:
  import psutil
except ImportError:
  print "Module 'psutil' required"


def cpu_percent():
  return psutil.cpu_percent(interval=10)


def cpu_percent_percpu():
  return psutil.cpu_percent(interval=10, percpu=True)


def _parse_cpu_times(cpu_time):
  return {
    'user': cpu_time.user,
    'nice': cpu_time.nice,
    'system': cpu_time.system,
    'idle': cpu_time.idle,
    'iowait': cpu_time.iowait,
    'irq': cpu_time.irq,
    'softirq': cpu_time.softirq,
    'steal': cpu_time.steal,
    'guest': cpu_time.guest,
    'guest_nice': cpu_time.guest_nice
  }


def cpu_times_percent():
  return _parse_cpu_times(psutil.cpu_times_percent())


def cpu_times_percent_percpu():
  values = []
  cpus = psutil.cpu_times_percent(interval=10, percpu=True)
  for cpu in cpus:
    values.append(
      _parse_cpu_times(cpu)
    )

  return values

