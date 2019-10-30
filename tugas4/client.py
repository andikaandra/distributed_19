import Pyro4
import base64
import json
import sys

namainstance = sys.argv[1] or "fileserver"

def get_fileserver_object():
    uri = "PYRONAME:{}@localhost:7777" . format(namainstance)
    fserver = Pyro4.Proxy(uri)
    return fserver

if __name__=='__main__':
    f = get_fileserver_object()
    f.create('a.txt')
    f.update('a.txt', content = open('a.txt','rb+').read() )

    f.create('b.txt')
    f.update('b.txt', content = open('b.txt','rb+').read())

    print(f.list())
    d = f.read('a.txt')
    open('a-kembali.txt','w+b').write(base64.b64decode(d['data']))

    k = f.read('b.txt')
    open('b-kembali.txt','w+b').write(base64.b64decode(k['data']))


