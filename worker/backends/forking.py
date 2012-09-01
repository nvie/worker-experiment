from __future__ import absolute_import
import os
import signal
import random
from .base import BaseWorker
from multiprocessing import Semaphore, Array


class ForkingWorker(BaseWorker):

    def __init__(self, num_processes=1):
        # Set up sync primitives, to communicate with the spawned children
        self._semaphore = Semaphore(num_processes)
        self._slots = Array('i', [0] * num_processes)

    def spawn_child(self):
        """Forks and executes the job."""
        self._semaphore.acquire()    # responsible for the blocking

        # Select an empty slot from self._slots (the first 0 value is picked)
        # The implementation guarantees there will always be at least one empty slot
        for slot, value in enumerate(self._slots):
            if value == 0:
                break

        # The usual hardcore forking action
        child_pid = os.fork()
        if child_pid == 0:
            # Within child

            # Disable signal handlers
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            signal.signal(signal.SIGTERM, signal.SIG_IGN)

            random.seed()
            try:
                self.fake_work()
            finally:
                # This is the new stuff.  Remember, we're in the child process
                # currently. When all work is done here, free up the current
                # slot (by writing a 0 in the slot position).  This
                # communicates to the parent that the current child has died
                # (so can safely be forgotten about).
                self._slots[slot] = 0
                self._semaphore.release()
                os._exit(0)
        else:
            # Within parent, keep track of the new child by writing its PID
            # into the first free slot index.
            self._slots[slot] = child_pid

    def wait_for_children(self):
        for child_pid in self._slots:
            if child_pid != 0:
                os.waitpid(child_pid, 0)

    def get_id(self):
        return os.getpid()
