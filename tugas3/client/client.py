import Pyro4
import Pyro4.errors
import time
import subprocess
import threading

interval = 0
server = None
connected = True

def ping_server(connected):
    while True:
        try:
            server._pyroBind()
        except:
            try:
                 server._pyroBind()
            except:
                print("=== Server disconnected | check by ping every {} seconds ===".format(interval))
                connected = False
            break
        time.sleep(interval)

def get_server():
    #ganti "localhost dengan ip yang akan anda gunakan sebagai server" 
    uri = "PYRONAME:greetserver@localhost:7777"
    gserver = Pyro4.Proxy(uri)
    return gserver

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
    thread = job_ping_server()
    while connected:
        req = input ("> ").lower()
        req_split = req.split()
        try:
            if req_split[0] == 'list':
                print(server.get_list_dir(req))
            elif req_split[0] == 'create':
                print(server.create_handler(req))
            elif req_split[0] == 'delete':
                print(server.delete_handler(req))
            elif req_split[0] == 'read':
                print(server.read_handler(req))
            elif req_split[0] == 'update':
                print(server.update_handler(req))
            elif req_split[0] == 'exit':
                print(server.bye())
                connected = False
            else:
                print(server.command_not_found())
        except Pyro4.errors.ConnectionClosedError:
            break

    thread.is_running = False
    thread.join()
    exit()