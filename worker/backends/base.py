import random
import time
import datetime


class BaseWorker(object):
    def work(self):
        stopped = False
        while not stopped:
            try:
                self.spawn_child()
            except KeyboardInterrupt:
                print 'Stopping on request.'
                stopped = True

        self.wait_for_children()

    def spawn_child(self):
        raise NotImplementedError('Implement this in a subclass.')

    def fake_work(self):
        sleep_time = 5 * random.random()
        print datetime.datetime.now(), '- Hello from', self.get_id(), '- %.3fs' % sleep_time
        time.sleep(sleep_time)
        print '                           - Goodbye from', self.get_id()
