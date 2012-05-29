#!/usr/bin/env python

from __future__ import print_function

import os

from twisted.internet import reactor, defer
from twisted.application import service

from .utils import yield_colorers, write_message
from .worker import Worker

class Boss(service.Service):
    def __init__(self, procmap):
        self.procmap = procmap
        self.workers = None
        self.colorers = None
        self.killall = None
    def startService(self):
        service.Service.startService(self)
        self.workers = {}
        self.colorers = yield_colorers()
        self.killall = False
        for tag, process in self.procmap.items():
            for index in range(process.concurrency):
                self.spawnWorker('%s.%d' % (tag, index+1), process.command)
    def stopService(self):
        service.Service.stopService(self)
        self.killEmAll()
        d = defer.DeferredList([protocol.deferred for protocol in self.workers.values()], consumeErrors=True)
        return d
    def spawnWorker(self, tag, command):
        protocol = Worker(tag, command, self.colorers.next())
        protocol.deferred.addCallback(self.workerDied)
        protocol.deferred.addErrback(lambda failure: self.workerFailed(protocol, failure))
        reactor.spawnProcess(
            protocol,
            '/bin/sh',
            ['/bin/sh'],
            env=os.environ,
        )
        self.workers[tag] = protocol
    def killEmAll(self):
        if not self.killall and self.workers:
            self.killall = True
            self.write_message("sending SIGTERM to all processes")
            for worker in self.workers.values():
                worker.terminate()
    def workerDied(self, protocol):
        del self.workers[protocol.tag]
        self.killEmAll()
        if not self.workers:
            reactor.stop()
    def workerFailed(self, protocol, failure):
        self.workerDied(protocol)
    def write_message(self, message):
        write_message(message, 'system')
