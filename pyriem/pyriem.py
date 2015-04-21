import time
import multiprocessing
import yaml
import bernhard
import argparse
import psutil
import signal
import sys
import os

__PROJECT__ = 'pyriem'
__VERSION__ = "0.1.22"

c = None
DEFAULT_FREQ = 5

print_only = False


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
    default_freq = DEFAULT_FREQ

    # Main loop
    for plugin, methods in plugins.iteritems():
        module = __import__('{namespace}.plugins.{plugin}'.format(namespace=__PROJECT__, plugin=plugin),
                            fromlist=[plugin])
        for method in methods:
            # Get module specific settings
            settings = config.get('{plugin}'.format(plugin=plugin), {}).get('{method}'.format(method=method), module._settings.get('{method}'.format(method=method), {}))

            method_frequency = config.get('{plugin}'.format(plugin=plugin), {}).get('{method}'.format(method=method), {}).get('freq', module._settings.get('{method}'.format(method=method), {}).get('freq', DEFAULT_FREQ))
            settings['freq'] = method_frequency

            timed_process = TimedProcess(method_frequency, module, method, config['default'], settings)
            timed_process.start()


def send(config, module, method, data):
    global c
    if not c:
        if config['transport'] == 'udp':
            c = bernhard.Client(host=config['host'], transport=bernhard.UDPTransport)
        else:
            c = bernhard.Client(host=config['host'])

    try:
        if type(data) is list:
            for item in data:
                if print_only:
                    print item
                else:
                    c.send(item)
        else:
            if print_only:
                print data
            else:
                c.send(data)

    except bernhard.TransportError:
        print "Could not reach server"


def kill_proc_tree(pid, including_parent=True):
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
        child.kill()
    if including_parent:
        parent.kill()


def kill_handler(signum, frame):
    print 'Signal handler called with signal', signum, frame
    kill_proc_tree(os.getpid())
    sys.exit()


def main():
    parser = argparse.ArgumentParser(
        description="A statistics collection framework for Riemann. Version {version}".format(version=__VERSION__))
    parser.add_argument('-c', '--config', help='Config file. Defaults /etc/pyriem.conf.', default='/etc/pyriem.conf')
    parser.add_argument('-d', '--debug', help='Specify plugin and method to run. ie -d load,one_minute')
    parser.add_argument('-p', '--printonly', help='Run as normal, however only print output, do not send',
                        action="store_true")

    namespace, sys_args = parser.parse_known_args()

    if namespace.debug:
        module, method = namespace.debug.split(',')
        module = __import__('{namespace}.plugins.{plugin}'.format(namespace=__PROJECT__, plugin=module),
                            fromlist=[module])
        results = getattr(module, method)()
        print results
        sys.exit()
    else:

        if namespace.printonly:
            global print_only
            print_only = True

        config_file = namespace.config if namespace.config else '/etc/pyriem.conf'

        config = yaml.load(file(config_file, 'r'))

        signal.signal(signal.SIGINT, kill_handler)
        signal.signal(signal.SIGTERM, kill_handler)
        signal.signal(signal.SIGHUP, kill_handler)

        try:
            collect(config)
        except (KeyboardInterrupt, SystemExit):
            kill_proc_tree(os.getpid())
            sys.exit()

