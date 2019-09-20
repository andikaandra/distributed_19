import Pyro4

def get_server():
    uri = "PYRONAME:greetserver@localhost:7777"
    gserver = Pyro4.Proxy(uri)
    return gserver

if __name__=='__main__':
    server = get_server()
    if server == None:
        exit()
    connected = True
    while connected:
        req = input ("> ").lower()
        req_split = req.split()
        if req_split[0] == 'list':
            print(server.get_list_dir(req))
        elif req_split[0] == 'create':
            print(server.create_handler(req))
        elif req_split[0] == 'delete':
            print(server.delete_handler(req))
        elif req_split[0] == 'read':
            print(server.read_handler(req))
        else:
            connected = False
