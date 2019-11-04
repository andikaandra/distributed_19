from file_server import Server
import Pyro4
import sys

def start_with_ns(nameinstance = "server"):
    # --- start 
    # pyro4-ns -n localhost -p 7777

    # --- list
    # pyro4-nsc -n localhost -p 7777 list
    __host = "localhost"
    __port = 7777
    server = Server()
    daemon = Pyro4.Daemon(host = __host)
    ns = Pyro4.locateNS(__host, __port)
    uri_server = daemon.register(server)
    print("URI server : ", uri_server)
    ns.register(nameinstance, uri_server)
    daemon.requestLoop()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        nameinstance = sys.argv[1]
        start_with_ns(nameinstance)
    else:
        start_with_ns()
