from __future__ import absolute_import
from gevent import monkey
monkey.patch_all()
import gevent.pool
from .base import BaseWorker


class GeventWorker(BaseWorker):

    def __init__(self, num_processes=1):
        self._pool = gevent.pool.Pool(num_processes)

    def spawn_child(self):
        """Forks and executes the job."""
        self._pool.spawn(self.fake_work)

    def wait_for_children(self):
        self._pool.join()

    def get_id(self):
        return id(gevent.getcurrent())
