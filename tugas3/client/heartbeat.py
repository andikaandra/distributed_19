import Pyro4
import time

class Heartbeat(object):
    def __init__(self, id):
        self.counter = 0
        self.last_received = time.time()
        self.id = id

    @Pyro4.expose
    def ok(self) -> str:
        return "ok"

    @Pyro4.expose
    def signal_heartbeat(self) -> str:
        self.counter = self.counter + 1
        self.last_received = time.time()
        return '> message from {} : counter {}, last received {}'.format(self.id, self.counter, self.last_received)

    