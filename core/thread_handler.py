from __future__ import annotations
import threading
from threading import Thread
from typing import List
import ctypes


class ThreadHandler:
    threads: List[ThisThread]

    def __init__(self):
        self.threads = []

    def add(self, thread: ThisThread):
        if thread not in self.threads:
            self.threads.append(thread)

    def remove(self, thread: ThisThread):
        if thread in self.threads:
            self.threads.remove(thread)

    # close the thread handler
    def close(self):
        for thread in self.threads:
            thread.raise_exception()
            thread.join()


thread_handler = ThreadHandler()


class ThisThread(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
        # add the created thread to the thread handler
        thread_handler.add_thread(self)

    # return the id of this thread
    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        # if this thread does not have id, find the id in all active items
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')
