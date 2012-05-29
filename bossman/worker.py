from __future__ import print_function

from twisted.internet import protocol, defer, reactor

from .utils import write_message

GRACE_PERIOD=3

class Worker(protocol.ProcessProtocol):
    def __init__(self, tag, command, colorer):
        self.tag = tag
        self.colorer = colorer
        self.deferred = defer.Deferred()
        self.transport = None
        self.timer = None
        self.command = command
    def makeConnection(self, transport):
        self.transport = transport
        self.transport.write("""trap "" INT\nexec %s""" % (self.command,))
        self.transport.closeChildFD(0)
        self.writeMessage('started with pid %s' % (transport.pid,))
    def processEnded(self, reason):
        self.writeMessage('process terminated')
        self.reason = reason
        if self.timer:
            self.timer.cancel()
        if not self.deferred.called:
            self.deferred.callback(self)
    def childDataReceived(self, fd, data):
        self.writeMessage(data)
    def __str__(self):
        return self.tag
    def __repr__(self):
        return '<%s: %s/%s/%s>' % (self.__class__.__name__, self, self.transport.pid, self.transport.status)
    def writeMessage(self, message):
        write_message(message, self.tag, self.colorer)
    def terminate(self, signal='TERM'):
        if not self.transport.pid:
            return
        self.transport.signalProcess(signal)
        if signal == 'TERM':
            self.alarm = reactor.callLater(GRACE_PERIOD, self.terminate, 'KILL')
        else:
            self.writeMessage("failed exiting after SIGTERM; sending SIGKILL and disowning")
            self.deferred.errback(self)
