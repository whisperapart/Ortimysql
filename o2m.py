#!/usr/bin/env python
# # -*- coding: utf-8 -*-


import os
import sys
import time
import unittest

from JDLibs.JDDaemon import JDDaemon as Daemon
from JDLibs.JDKafkaConsumer import Consumer as Consumer


class JDKFKCDaemon(Daemon):
    def __init__(self, *args, **kwargs):
        super(JDKFKCDaemon, self).__init__(*args, **kwargs)

    def run(self, force=False):
        while True:
            com = Consumer(verbose=0, forceRestart=force)
            com.run()
            com.close()
            force = False   # force init only for ONE FUCKING TIME
            time.sleep(0.3)

    def stop(self):
        # self.com.close()
        super(JDKFKCDaemon, self).stop()

    def status(self):
        pid = self.get_pid()
        if pid is None:
            self.log('Process is stopped')
            return False
        elif os.path.exists('JDKFKCDaemon.pid'):
            self.log('Process (pid %d) is running...' % pid)
            return True
        else:
            self.log('Process (pid %d) is killed' % pid)
            return False


class TDaemon(Daemon):
    def __init__(self, *args, **kwargs):
        super(TDaemon, self).__init__(*args, **kwargs)
        testoutput = open('testing_daemon', 'a')
        testoutput.write('inited')
        testoutput.close()

    def run(self):
        cnt = 0
        while True:
            cnt = cnt + 1
            testoutput = open('testing_daemon', 'a')
            testoutput.write('%s\n' % cnt)
            testoutput.close()
            time.sleep(0.3)

    def status(self):
        pid = self.get_pid()
        if pid is None:
            self.log('Process is stopped')
            return False
        elif os.path.exists('testing_daemon.pid'):
            self.log('Process (pid %d) is running...' % pid)
            return True
        else:
            self.log('Process (pid %d) is killed' % pid)
            return False


def main():
    if len(sys.argv) == 1:
        print('Usage: python filename.py [option]\n'
              '\t\033[0;32;40m start \033[0m\t\tstart daemon\n'
              '\t\033[0;31;40m stop \033[0m\t\tstop daemon\n'
              '\t\033[0;36;40m restart \033[0m\trestart\n'
              '\t\033[0;33;40m status \033[0m\tcheck status\n'
              '\t\033[0;34;40m forceInit \033[0m\tredo queue')
    elif len(sys.argv) == 2:
        arg = sys.argv[1]
        if arg in ('start', 'stop', 'restart', 'status'):
            d = JDKFKCDaemon('JDKFKCDaemon.pid', verbose=1)
            getattr(d, arg)()
        elif arg == 'forceInit':
            d = JDKFKCDaemon('JDKFKCDaemon.pid', verbose=1)
            d.start(force=True)


if __name__ == '__main__':
    main()
