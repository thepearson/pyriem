import time
import multiprocessing
import yaml
import bernhard
import argparse
import signal
import sys

__PROJECT__ = 'pyriem'
__VERSION__ = "0.1.12"

c = None
running_procs = []

class TimedProcess(multiprocessing.Process):
  def __init__(self, interval, module, method, config, settings=None):
    multiprocessing.Process.__init__(self)
    self.interval = interval
    self.module = module
    self.method = method
    self.config = config
    self.settings = settings

  def run(self):
    while True:
      results = getattr(self.module, self.method)(self.settings)
      send(self.config, self.module, self.method, results)
      time.sleep(self.interval)


def collect(config):
  global running_procs
  plugins = config['enabled plugins']
  default_freq = config['default']['frequency']

  # Main loop
  for plugin, methods in plugins.iteritems():
    module = __import__('{namespace}.plugins.{plugin}'.format(namespace=__PROJECT__, plugin=plugin), fromlist=[plugin])
    for method in methods:
      try:
        method_frequency = config['{plugin}'.format(plugin=plugin)]['{method}'.format(method=method)]['frequency']
      except:
        method_frequency = default_freq

      timed_process = TimedProcess(method_frequency, module, method, config, config['{plugin}'.format(plugin=plugin)]['{method}'.format(method=method)])
      running_procs.append(timed_process)
      timed_process.start()



#
# def execute(module, method, config, settings=None):
#   results = getattr(module, method)(settings)
#   return send(config, module, method, results)

def send(config, module, method, data):
  global c
  if not c:
    if config['default']['transport'] == 'udp':
      c = bernhard.Client(host=config['default']['host'], transport=bernhard.UDPTransport)
    else:
      c = bernhard.Client(host=config['default']['host'])

  if type(data) is list:
    for item in data:
      c.send(item)
  else:
    c.send(data)
  q = c.query('true')


def clean_up():
  global running_procs
  print('Shutting down all processes')
  for proc in running_procs:
    proc.terminate()

  sys.exit(0)


def main():
  parser = argparse.ArgumentParser(description="A statistics collection framework for Riemann. Version {version}".format(version=__VERSION__))
  parser.add_argument('-c', '--config', help='Config file. Defaults /etc/pyriem.conf.', default='/etc/pyriem.conf')

  namespace, sys_args = parser.parse_known_args()
  config_file = namespace.config if namespace.config else '/etc/pyriem.conf'

  config = yaml.load(file(config_file, 'r'))

  try:
    collect(config)
  except (KeyboardInterrupt, SystemExit):
    clean_up()
    sys.exit()

