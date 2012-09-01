def Worker(type=None, *args, **kwargs):
    if type is None or type == 'forking':
        from .backends.forking import ForkingWorker
        return ForkingWorker(*args, **kwargs)
    elif type == 'gevent':
        from .backends.gevent import GeventWorker
        return GeventWorker(*args, **kwargs)
    else:
        raise ValueError('Unknown worker type: %s' % (type,))
