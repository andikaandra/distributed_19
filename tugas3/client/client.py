import Pyro4
import Pyro4.errors
import time
import threading
import os
import sys

interval = 0
server = None
connected = True

def get_server():
    #ganti "localhost dengan ip yang akan anda gunakan sebagai server" 
    uri = "PYRONAME:greetserver@localhost:7777"
    gserver = Pyro4.Proxy(uri)
    return gserver

def ping_server(connected):
    while True:
        try:
            res = server.ok()
            if res.value == 'ok':
                pass
        except:
            print("\nserver is down")
            break
        time.sleep(interval)

def gracefully_exits():
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

def job_ping_server():
    global connected
    t = threading.Thread(target=ping_server, args =(lambda : connected, ))
    t.start()
    return t

if __name__=='__main__':
    server = get_server()
    if server == None:
        exit()
    
    interval = server.ping_interval()
    server._pyroTimeout = interval
    server._pyroAsync()
    thread = job_ping_server()
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
            elif req_split[0] == 'down':
                res = server.down_my_server()
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
            print("disconnecting..")
            break
        except KeyboardInterrupt:
            print('Interrupted..')
            break
    connected = False
    thread.join()
    gracefully_exits()