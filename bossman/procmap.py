class Procdef(object):
    attributes = dict(command=str, concurrency=int)
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    def __setattr__(self, key, value):
        try:
            value = self.attributes[key](value)
        except KeyError:
            raise TypeError('unexpected argument %r' % (key,))
        except ValueError:
            raise TypeError("%r is not of the type %r" % (key, self.attributes[key].__name__))
        super(Procdef, self).__setattr__(key, value)

def parse_procmap(handle):
    procmap = {}
    for line in handle:
        tag, command = line.split(':', 1)
        procmap[tag.strip()] = Procdef(command=command.strip(), concurrency=1)
    return procmap
