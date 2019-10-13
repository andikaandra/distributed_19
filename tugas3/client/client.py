import Pyro4
import Pyro4.errors
import time
import threading
import os
import sys
import uuid
from heartbeat import Heartbeat

id = None
interval = 0
server = None
connected = True

def get_server(id):
    try:
        uri = "PYRONAME:{}@localhost:7777".format(id)
        gserver = Pyro4.Proxy(uri)
        return gserver
    except:
        gracefully_exits()

def job_heartbeat() -> threading.Thread:
    global id
    heartbeat = Heartbeat(id)
    t1 = threading.Thread(target=job_heartbeat_failure, args=(heartbeat,))
    t1.start()

    t = threading.Thread(target=expose_function_heartbeat, args=(heartbeat, id,))
    t.start()
    return heartbeat, t, t1

def job_heartbeat_failure(heartbeat):
    while True:
        if time.time() - heartbeat.last_received > 2*interval:
            print("\nserver is down [DETECT BY heartbeat]")
            break
        time.sleep(interval)
    gracefully_exits()

def job_heartbeat_failure_all_to_all(id):
    server_heartbeat = get_server('heartbeat-{}'.format(id))
    while True:
        try:
            summary = server_heartbeat.get_summary_heartbeat(id)
            summary = summary.split(',')
            if summary[1] == 'none':
                pass
            else:
                if time.time() - float(summary[2]) > 2*interval:
                    print("\n{} is down [DETECT BY all heartbeat]\n> ".format(id))
                    break        
            time.sleep(interval)
        except:
            print("\n{} is down [DETECT BY all heartbeat]\n> ".format(id))
            break

def expose_function_heartbeat(heartbeat, id):
    __host = "localhost"
    __port = 7777
    daemon = Pyro4.Daemon(host = __host)
    ns = Pyro4.locateNS(__host, __port)
    uri_server = daemon.register(heartbeat)
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
                print("\nserver is down [DETECT BY ping ack]")
                break
        time.sleep(interval)
    gracefully_exits()

def job_ping_server_ping_ack() -> threading.Thread:
    t = threading.Thread(target=ping_server)
    t.start()
    return t

def gracefully_exits():
    # unregister device on server 
    server.connected_device_delete(id)
    print("disconnecting..")
    time.sleep(0.5)
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

def clear_connected_device(devices, id) -> list:
    if id in devices:
        devices.remove(id)
    return devices

def all_to_al_heartbeat_job(heartbeat, devices):
    for device in devices:
        heartbeat.new_thread_job(device)

        t1 = threading.Thread(target=job_heartbeat_failure_all_to_all, args=(device,))
        t1.start()

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
    server = get_server('server')
    interval = server.ping_interval()
    server._pyroTimeout = interval
    server._pyroAsync()

    # register device on server (heartbeat)
    server.connected_device_add(id)

    heartbeat, thread_heartbeat, thread_heartbeat_detector = job_heartbeat()
    thread_ping_ack = job_ping_server_ping_ack()

    # register failure detector on server
    server.new_thread_job(id)

    conn_device = server.connected_device_ls()
    conn_device.ready
    conn_device.wait(1)
    conn_device = clear_connected_device(conn_device.value.split(','), id)

    all_to_al_heartbeat_job(heartbeat, conn_device)

    listen_command()

    connected = False
    thread_ping_ack.join()
    # thread_heartbeat.join()
    # thread_heartbeat_detector.join()
    gracefully_exits()