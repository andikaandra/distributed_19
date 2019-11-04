import shlex
import os
import Pyro4
import time

class GlobalServer(object):
    def __init__(self):
        self.connected_server = []
    
    @Pyro4.expose
    def add_connected_server(self, server_name):
        self.connected_server.append(server_name)

    @Pyro4.expose
    def remove_connected_server(self, server_name):
        self.connected_server.remove(server_name)

    @Pyro4.expose
    def get_all_connected_server(self) -> str:
        return ",".join(self.connected_server)

    @Pyro4.expose
    def check_connected_server(self, server_name) -> bool:
        return server_name in self.connected_server

if __name__ == "__main__":
    __host = "localhost"
    __port = 7777
    with Pyro4.Daemon(host = __host) as daemon:
        global_server = GlobalServer()
        ns = Pyro4.locateNS(__host, __port)
        uri_server = daemon.register(global_server)
        print("URI server : ", uri_server)
        ns.register("globalserver", uri_server)
        daemon.requestLoop()
    print('\nglobal server exited..')
