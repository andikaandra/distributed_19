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

    def thread_read_queue(self):
        t = threading.Thread(target=self.queue_start)
        t.start()

    def __root_folder_exists(self, root):
        if not os.path.exists(root):
            os.makedirs(root)

    def __get_storage_path(self, server) -> str:
        root = os.path.dirname(os.path.abspath(__file__)) + "/storage/" + server
        self.__root_folder_exists(root)
        return root

    def __get_list_dir(self, server):
        root = self.__get_storage_path(server)
        return os.listdir(root), root
    
    def __process_file(self, spath, sname, tpath, operation):
        sf = open(os.path.join(spath, sname), 'r')
        data = sf.read()
        with open(os.path.join(tpath, sname), operation) as f:
            f.write(data)

    @Pyro4.expose
    def sync_between_servers(self):
        for i, val in enumerate(self.connected_server):
            for server in range(i+1, len(self.connected_server)):
                source_dir, source_path = self.__get_list_dir(val)
                _, target_path = self.__get_list_dir(self.connected_server[server])
                for sfile in source_dir:
                    self.__process_file(source_path, sfile, target_path, 'w')
                

    def queue_start(self):
        while True:
            need_to_sync = False
            item = self.queue_manager.get()
            command = item['command']
            req = item['req']
            for server in self.connected_server:
                if server == item['server']:
                    continue
                try:
                    server_instance = Server(server, False)
                    if command == 'create':
                        server_instance.create_handler(req)
                    elif command == 'update':
                        server_instance.update_handler(req)
                    elif command == 'delete':
                        server_instance.delete_handler(req)
                    print('run : {} | {} on {}'.format(command, req, server))
                except:
                    print('failed sync : {} | {} on {}'.format(command, req, server))
                    need_to_sync = True
                    continue
            if need_to_sync:
                self.sync_between_servers()
    
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
