from file_server import Server
import Pyro4
import sys

globalserver = None

def get_global_server(name = "globalserver"):
    try:
        uri = "PYRONAME:{}@localhost:7777".format(name)
        gserver = Pyro4.Proxy(uri)
        return gserver
    except:
        sys.exit(0)

def start_with_ns(nameinstance = "server"):
    # --- start 
    # pyro4-ns -n localhost -p 7777

    # --- list
    # pyro4-nsc -n localhost -p 7777 list
    __host = "localhost"
    __port = 7777
    if not globalserver.check_connected_server(nameinstance):
        globalserver.add_connected_server(nameinstance)
        with Pyro4.Daemon(host = __host) as daemon:
            print("connected server : {}".format(globalserver.get_all_connected_server()))
            server = Server(nameinstance)
            ns = Pyro4.locateNS(__host, __port)
            uri_server = daemon.register(server)
            print("URI server : ", uri_server)
            ns.register(nameinstance, uri_server)
            daemon.requestLoop()
        print('\nexited..')
        print('unregister {} from global server'.format(nameinstance))
        globalserver.remove_connected_server(nameinstance)
    else:
        print("server {} already running".format(nameinstance))


if __name__ == '__main__':
    globalserver = get_global_server()
    if len(sys.argv) > 1:
        nameinstance = sys.argv[1]
        start_with_ns(nameinstance)
    else:
        start_with_ns()
