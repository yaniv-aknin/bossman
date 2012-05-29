#!/usr/bin/env python

from __future__ import print_function

import signal
import os
import sys
import argparse

from twisted.internet import reactor

from .boss import Boss
from .procmap import parse_procmap

def parse_arguments(argv):
    parser = argparse.ArgumentParser(prog=os.path.basename(argv[0]))
    parser.add_argument('-f', '--procfile', default='Procfile')
    options = parser.parse_args(argv[1:])

    try:
        options.procfile = open(options.procfile)
    except IOError:
        print('%s: failed opening %s' % (parser.prog, options.procfile), file=sys.stderr)
        sys.exit(1)

    return options

def patch_sigint():
    old_sigint = signal.getsignal(signal.SIGINT)
    def new_sigint(signum, frame):
        print('SIGINT received', file=sys.stderr)
        return old_sigint(signum, frame)
    signal.signal(signal.SIGINT, new_sigint)

def run(options):
    with options.procfile as handle:
        procmap = parse_procmap(handle)
    boss = Boss(procmap)
    reactor.callWhenRunning(boss.startService)
    reactor.callWhenRunning(patch_sigint)
    reactor.addSystemEventTrigger("before", "shutdown", boss.stopService)
    reactor.run()

def main():
    run(parse_arguments(sys.argv))
