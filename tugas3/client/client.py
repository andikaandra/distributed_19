import Pyro4
import Pyro4.errors
import time
import subprocess
import threading
import os
import sys

server = None
connected = True

def get_server():
    #ganti "localhost dengan ip yang akan anda gunakan sebagai server" 
    uri = "PYRONAME:greetserver@localhost:7777"
    gserver = Pyro4.Proxy(uri)
    return gserver

def gracefully_exits():
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

if __name__=='__main__':
    server = get_server()
    if server == None:
        exit()
    server._pyroTimeout = server.ping_interval()
    server._pyroAsync()
    while connected:
        try:
            req = input ("> ").lower()
            req_split = req.split()

            if req_split[0] == 'list':
                res = server.get_list_dir(req)
            elif req_split[0] == 'create':
                res = server.create_handler(req)
            elif req_split[0] == 'delete':
                res = server.delete_handler(req)
            elif req_split[0] == 'read':
                res = server.read_handler(req)
            elif req_split[0] == 'update':
                res = server.update_handler(req)
            elif req_split[0] == 'exit':
                print(server.bye())
                connected = False
            else:
                res = server.command_not_found()

            # ready = res.ready
            # res.wait(timeout=3)
            # while not ready:
            #     ready = res.ready
            #     print("loading..")
            print(res.value)
        except (Pyro4.errors.ConnectionClosedError, Pyro4.errors.CommunicationError) as e:
            print(str(e))
            break
        except KeyboardInterrupt:
            print('Interrupted..')
            break
    gracefully_exits()