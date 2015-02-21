try:
  import os
except ImportError:
  print "Requirement: 'os' module not found."


try:
  import psutil
except ImportError:
  print "Module 'psutil' required"


def host_info():
  """ Returns the operating system load as (1min, 5min, 15min)
  """
  uname = os.uname()

  try:
      cpu_count = psutil.cpu_count()
  except AttributeError:
      cpu_count = psutil.NUM_CPUS

  return (
      uname[0],
      uname[1],
      uname[2],
      cpu_count,
      psutil.virtual_memory().total,
      psutil.swap_memory().total,
      int(psutil.get_boot_time())
  )
