import subprocess
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

    def bye(self) -> str:
        return "bye!"

    def delete_file(self, path, name) -> str:
        res = self.command_success()
        try:
            os.remove(os.path.join(path, name))
        except Exception as e:
            return str(e)
        return res

    def _process_file(self, path, name, operation, *args, **kwargs) -> str:
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
    
    def _root_folder_exists(self, root):
        if not os.path.exists(root):
            os.makedirs(root)

    def _get_storage_path(self) -> str:
        root = os.path.dirname(os.path.abspath(__file__)) + "/storage"
        self._root_folder_exists(root)
        return root

    def get_list_dir(self, req) -> str:
        args = req.split()
        dirs = os.listdir(self._get_storage_path())
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
    
    def create_handler(self, req) -> str:
        args = shlex.split(req)        
        dirs = self._get_storage_path()
        res = ""
        if len(args) > 1:
            for file_name in args[1:]:
                res = self._process_file(dirs, file_name, "w+")
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
            res = self._process_file(dirs, args[1], "r")
        else:
            res = self.command_not_found()
        return res

    def update_handler(self, req):
        args = shlex.split(req)        
        dirs = self._get_storage_path()
        res = ""
        if len(args) == 4:
            if args[1] in ["--append", "-a"]:
                res = self._process_file(dirs, args[2], "a+", content=args[3])
            elif args[1] in ["--overwrite", "-o"]:
                res = self._process_file(dirs, args[2], "w")
                res = self._process_file(dirs, args[2], "a+", content=args[3])
            else:
                res = self.command_not_found()
        else:
            res = self.command_not_found()
        return res