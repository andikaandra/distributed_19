import Pyro4
import Pyro4.errors
import time
import threading
import os
import sys
import uuid

id = None
interval = 0
server = None
connected = True

def get_server():
    try:
        uri = "PYRONAME:server@localhost:7777"
        gserver = Pyro4.Proxy(uri)
        return gserver
    except:
        gracefully_exits()

def expose_function(Server, id):
    __host = "localhost"
    __port = 3001
    daemon = Pyro4.Daemon(host = __host)
    ns = Pyro4.locateNS(__host, __port)
    x_Server = Pyro4.expose(Server)
    uri_server = daemon.register(x_Server)
    ns.register("heartbeat-{}".format(id), uri_server)
    daemon.requestLoop()

def communicate() -> bool:
    try:
        res = server.ok()
        if res.value == 'ok':
            pass
    except:
        return False
    return True

def ping_server():
    global connected
    while True and connected:
        alive = communicate()
        if not alive:
            alive = communicate()
            if not alive:
                print("\nserver is down")
                break
        time.sleep(interval)
    gracefully_exits()

def job_ping_server_ping_ack() -> threading.Thread:
    t = threading.Thread(target=ping_server)
    t.start()
    return t

def gracefully_exits():
    server.connected_device_delete(id)
    time.sleep(0.5)
    print("disconnecting..")
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

def listen_command():
    alive = True
    while alive:
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
            elif req_split[0] == 'cd':
                res = server.connected_device_list()
            elif req_split[0] == 'exit':
                res = server.bye()
                alive = False
            elif req_split[0] == 'down':
                res = server.down_my_server()
            else:
                res = server.command_not_found()

            print(res.value)
        except (Pyro4.errors.ConnectionClosedError, Pyro4.errors.CommunicationError) as e:
            print(str(e))
            break
        except KeyboardInterrupt:
            print('Interrupted..')
            break
    return

if __name__=='__main__':
    # device id 
    id = str(uuid.uuid4())
    print('---------- registered id : {}'.format(id))

    # core
    server = get_server()
    interval = server.ping_interval()
    server._pyroTimeout = interval
    server._pyroAsync()

    # register device on server 
    server.connected_device_add(id)

    # create heartbeat obj 
    # expose_function(None, id)

    thread_ping_ack = job_ping_server_ping_ack()
    listen_command()
    connected = False
    thread_ping_ack.join()
    gracefully_exits()