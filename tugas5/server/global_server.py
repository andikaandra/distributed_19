import shlex
import os
import Pyro4
import time
import queue
import threading
from file_server import Server

class GlobalServer(object):
    def __init__(self):
        self.connected_server = []
        self.queue_manager = queue.Queue()
    
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

    @Pyro4.expose
    def push_to_queue(self, command, req, nameserver):
        data = {'command': command, 'req': req, 'server' : nameserver}
        dc = data.copy()
        self.queue_manager.put(dc)
        data.clear()

    def sync_between_servers(self):
        for idx, val in enumerate(self.connected_server):
            print(idx, val)
            

    def thread_read_queue(self):
        t = threading.Thread(target=self.queue_start)
        t.start()

    def queue_start(self):
        while True:
            item = self.queue_manager.get()
            # todo : tell all server to replicate
            command = item['command']
            req = item['req']
            for server in self.connected_server:
                if server == item['server']:
                    continue
                server_instance = Server(server, False)
                if command == 'create':
                    server_instance.create_handler(req)
                elif command == 'update':
                    server_instance.update_handler(req)
                elif command == 'delete':
                    server_instance.delete_handler(req)
                print('run : {} | {} on {}'.format(command, req, server))
    
    # test 
    @Pyro4.expose
    def get_all_queue(self):
        temp = []
        for n in list(self.queue_manager.queue):
            temp.append(n['command'])
        return ",".join(temp)
        

if __name__ == "__main__":
    __host = "localhost"
    __port = 7777
    with Pyro4.Daemon(host = __host) as daemon:
        global_server = GlobalServer()
        global_server.thread_read_queue()
        ns = Pyro4.locateNS(__host, __port)
        uri_server = daemon.register(global_server)
        print("URI server : ", uri_server)
        ns.register("globalserver", uri_server)
        daemon.requestLoop()
    print('\nglobal server exited..')
