import random
import shlex
import os

class GreetServer(object):
    def __init__(self):
        pass

    def command_not_found(self):
        return "command not found"

    def command_success(self):
        return "operation success"

    def delete_file(self, path, name) -> str:
        res = self.command_success()
        try:
            full_path = os.path.join(path, name)
            os.remove(full_path)
        except Exception as e:
            return str(e)
        return res

    def process_file(self, path, name, operation, *args, **kwargs) -> str:
        res = self.command_success()
        try:
            content = kwargs.get('content', None)
            full_path = os.path.join(path, name)
            f = open(full_path, operation)
            if operation == "r":
                res = f.read()
            f.close()
        except Exception as e:
            return str(e)
        return res
            
    def _get_storage_path(self) -> str:
        root = os.path.dirname(os.path.abspath(__file__))
        return root + "/storage"

    def get_list_dir(self, req) -> list:
        args = req.split()
        dirs = os.listdir(self._get_storage_path())
        res = ""
        if len(args) == 1 :
            for dir in dirs:
                res = res + "{}   ".format(dir)
        elif len(args) == 2 and args[1] in ["-a", "-all"]:
            for dir in dirs:
                res = res + "{}\n".format(dir)
        else:
            res = self.command_not_found()
        return res
    
    def create_handler(self, req) -> str:
        args = shlex.split(req)        
        dirs = self._get_storage_path()
        res = ""
        if len(args) > 1:
            for file_name in args[1:]:
                res = self.process_file(dirs, file_name, "w+")
                if res != self.command_success():
                    return res
        else:
            res = self.command_not_found()
        return res

    def delete_handler(self, req) -> str:
        args = shlex.split(req)        
        dirs = self._get_storage_path()
        res = ""
        if len(args) > 1:
            for file_name in args[1:]:
                res = self.delete_file(dirs, file_name)
                if res != self.command_success():
                    return res
        else:
            res = self.command_not_found()
        return res

    def read_handler(self, req) -> str:
        args = shlex.split(req)        
        dirs = self._get_storage_path()
        res = ""
        if len(args) > 1:
            res = self.process_file(dirs, args[1], "r")
        else:
            res = self.command_not_found()
        return res