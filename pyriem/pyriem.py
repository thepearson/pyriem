import time
import threading
import yaml
import bernhard
import argparse

__PROJECT__ = 'pyriem'
__VERSION__ = "0.1.9"

c = None

def collect(config):
  plugins = config['enabled plugins']
  default_freq = config['default']['frequency']
  last_runs = {}

  # Main loop
  while True:
    current_time = time.time()
    for plugin, methods in plugins.iteritems():
      module = __import__('{namespace}.plugins.{plugin}'.format(namespace=__PROJECT__, plugin=plugin), fromlist=[plugin])
      for method in methods:
        try:
          method_frequency = config['{plugin}'.format(plugin=plugin)]['{method}'.format(method=method)]['frequency']
        except:
          method_frequency = default_freq
        if method in last_runs:
          method_last_run = last_runs[method]
        else:
          method_last_run = 0
        if (method_last_run + method_frequency) <= current_time:
          thread = threading.Thread(target=execute, args=(module, method, config, config['{plugin}'.format(plugin=plugin)]['{method}'.format(method=method)]))
          thread.start()
          last_runs[method] = current_time
    time.sleep(1)


def execute(module, method, config, settings=None):
  results = getattr(module, method)(settings)
  return send(config, module, method, results)


def send(config, module, method, data):
  global c
  if not c:
    c = bernhard.Client(host=config['default']['host'])

  if type(data) is list:
    for item in data:
      c.send(item)
  else:
    c.send(data)
  q = c.query('true')


def main():
  parser = argparse.ArgumentParser(description="A statistics collection framework for Riemann. Version {version}".format(version=__VERSION__))
  parser.add_argument('-c', '--config', help='Config file. Defaults /etc/pyriem.conf.', default='/etc/pyriem.conf')

  namespace, sys_args = parser.parse_known_args()
  config_file = namespace.config if namespace.config else '/etc/pyriem.conf'

  config = yaml.load(file(config_file, 'r'))
  collect(config)
