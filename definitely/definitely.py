from dataclasses import dataclass
from itertools import repeat
from collections import defaultdict
from multiprocessing import Process, Queue
from threading import Thread, Lock
from inspect import isgeneratorfunction
from time import time, sleep
from copy import copy

class DefinitelyRunnable:
    def __init__(self, id, *, target, args=tuple(), kwargs=dict(), timeout=None, times=None, interval=None):
        self.id = id
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self.timeout = timeout
        self.times = times
        self.interval = interval

    def report(self, queue, kind, data):
        queue.put((self.id, kind, time(), data))

    def _loop_iteration(self, output_queue: Queue):
        if isgeneratorfunction(self.target):
            for result in self.target(*self.args, **self.kwargs):
                self.report(output_queue, 'yield', result)
        else:
            result = self.target(*self.args, **self.kwargs)
            self.report(output_queue, 'return', result)

    def run(self, output_queue: Queue):
        if self.times:
            runs = repeat(None, self.times)
        else:
            runs = repeat(None)

        for _ in runs:
            self.report(output_queue, 'start', None)

            try:
                self._loop_iteration(output_queue)
            except Exception as e:
                self.report(output_queue, 'exception', e)

            self.report(output_queue, 'finish', None)
            if self.interval:
                sleep(self.interval)

        self.report(output_queue, 'exited', None)

class Definitely:
    def __init__(self):
        self.runnables = {}
        self.procs = {}
        self.runnables_lock = Lock()
        self.input_queue = Queue()
        self.output_queue = Queue()
        self.last_seens = defaultdict(time)

        Thread(target=self._check, daemon=True).start()
        Thread(target=self._eat, daemon=True).start()

    def run(self, id, func, **kwargs):
        runnable = DefinitelyRunnable(id, target=func, **kwargs)
        with self.runnables_lock:
            self.runnables[id] = runnable
        self._start(runnable.id)

    def monitor(self, topics=('return', 'yield')):
        while True:
            id, topic, timestamp, result = self.output_queue.get()
            if topic in topics:
                yield id, topic, timestamp, result

    def _eat(self):
        while True:
            packet = self.input_queue.get()
            id, topic, timestamp, result = packet
            self.output_queue.put(packet)

            self.last_seens[id] = timestamp

    def _check(self):
        while True:
            # Use 40% of lowest timeout as sleep duration, or clamp to at most 1 sec
            minimal_timeout = 1
            with self.runnables_lock:
                runnables = self.runnables

            for id, runnable in runnables.items():
                if runnable.timeout is not None:
                    minimal_timeout = min(minimal_timeout, runnable.timeout or 0)
                    last_seen = self.last_seens[id]
                    if time() - last_seen > runnable.timeout:
                        self._stop(id)
                        self._start(id)
            sleep(0.4*minimal_timeout)

    def _start(self, id):
        with self.runnables_lock:
            runnable = self.runnables[id]
        self.procs[id] = Process(target=runnable.run, args=(self.input_queue,),  daemon=True)
        self.procs[id].start()

    def _stop(self, id):
        proc = self.procs[id]
        proc.terminate()

if __name__=='__main__':
    pass
