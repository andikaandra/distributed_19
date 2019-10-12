import shlex
import os
import time
import Pyro4
import json

class Server(object):
    def __init__(self):
        self.connected_device = []

    @Pyro4.expose
    def connected_device_list(self) -> str:
        return 'connected device : '+', '.join(self.connected_device)

    @Pyro4.expose
    def connected_device_add(self, id) -> str:
        print('register '+ id)
        self.connected_device.append(id)
        self.ok()

    @Pyro4.expose
    def connected_device_delete(self, id) -> str:
        print('unregister '+ id)
        self.connected_device.remove(id)
        self.ok()

    @Pyro4.expose
    def command_not_found(self) -> str:
        return "command not found"

    @Pyro4.expose
    def command_success(self) -> str:
        return "operation success"

    @Pyro4.expose
    def bye(self) -> str:
        return "bye!"

    @Pyro4.expose
    def ok(self) -> str:
        return "ok"

    @Pyro4.expose
    def fail(self) -> str:
        return "fail"

    @Pyro4.expose
    def ping_interval(self) -> int:
        return 3

    @Pyro4.expose
    def max_retries(self) -> int:
        return 2

    def __delete_file(self, path, name) -> str:
        res = self.command_success()
        try:
            os.remove(os.path.join(path, name))
        except Exception as e:
            return str(e)
        return res

    def __process_file(self, path, name, operation, *args, **kwargs) -> str:
        res = self.command_success()
        try:
            f = open(os.path.join(path, name), operation)
            if operation == "r":
                res = f.read()
            elif operation == "a+":
                f.write(kwargs.get('content', None))
            f.close()
        except Exception as e:
            return str(e)
        return res
    
    def __root_folder_exists(self, root):
        if not os.path.exists(root):
            os.makedirs(root)

    def __get_storage_path(self) -> str:
        root = os.path.dirname(os.path.abspath(__file__)) + "/storage"
        self.__root_folder_exists(root)
        return root

    @Pyro4.expose
    def get_list_dir(self, req) -> str:
        args = req.split()
        dirs = os.listdir(self.__get_storage_path())
        res = ""
        if len(args) == 1 :
            for dir in dirs:
                res = res + "{}   ".format(dir)
        elif len(args) == 2 and args[1] in ["-a", "-all"]:
            res = res + "."
            for dir in dirs:
                res = res + "\n{}".format(dir)
        else:
            res = self.command_not_found()
        return res
    
    @Pyro4.expose
    def create_handler(self, req) -> str:
        args = shlex.split(req)        
        dirs = self.__get_storage_path()
        res = ""
        if len(args) > 1:
            for file_name in args[1:]:
                res = self.__process_file(dirs, file_name, "w+")
                if res != self.command_success():
                    return res
        else:
            res = self.command_not_found()
        return res

    @Pyro4.expose
    def delete_handler(self, req) -> str:
        args = shlex.split(req)        
        dirs = self.__get_storage_path()
        res = ""
        if len(args) > 1:
            for file_name in args[1:]:
                res = self.__delete_file(dirs, file_name)
                if res != self.command_success():
                    return res
        else:
            res = self.command_not_found()
        return res

    @Pyro4.expose
    def read_handler(self, req) -> str:
        args = shlex.split(req)        
        dirs = self.__get_storage_path()
        res = ""
        if len(args) > 1:
            res = self.__process_file(dirs, args[1], "r")
        else:
            res = self.command_not_found()
        return res

    @Pyro4.expose
    def update_handler(self, req):
        args = shlex.split(req)        
        dirs = self.__get_storage_path()
        res = ""
        if len(args) == 4:
            if args[1] in ["--append", "-a"]:
                res = self.__process_file(dirs, args[2], "a+", content=args[3])
            elif args[1] in ["--overwrite", "-o"]:
                res = self.__process_file(dirs, args[2], "w")
                res = self.__process_file(dirs, args[2], "a+", content=args[3])
            else:
                res = self.command_not_found()
        else:
            res = self.command_not_found()
        return res

    @Pyro4.expose
    def down_my_server(self) -> str:
        time.sleep(self.ping_interval() + 1)
        return self.ok()