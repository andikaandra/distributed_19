from fileserver import  *
import Pyro4
import sys

def start_without_ns():
    daemon = Pyro4.Daemon()
    x_FileServer = Pyro4.expose(FileServer)
    uri = daemon.register(x_FileServer)
    print("my URI : ", uri)
    daemon.requestLoop()


def start_with_ns(nameinstance = "fileserver"):
    #name server harus di start dulu dengan  pyro4-ns -n localhost -p 7777
    #untuk mengetahui instance apa saja yang aktif gunakan pyro4-nsc -n localhost -p 7777 list

    daemon = Pyro4.Daemon(host="localhost")
    ns = Pyro4.locateNS("localhost",7777)
    x_FileServer = Pyro4.expose(FileServer)
    uri_fileserver = daemon.register(x_FileServer)
    ns.register("{}" . format(nameinstance), uri_fileserver)
    #ns.register("fileserver2", uri_fileserver)
    #ns.register("fileserver3", uri_fileserver)
    daemon.requestLoop()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        nameinstance = sys.argv[1]
        start_with_ns(nameinstance)
    else:
        start_with_ns()
