import os
import base64

class FileServer(object):
    def __init__(self):
        pass

    def create_return_message(self,kode='000',message='kosong',data=None):
        return dict(kode=kode,message=message,data=data)

    def list(self):
        print("list ops")
        try:
            daftarfile = []
            for x in os.listdir(self.__get_storage_path()):
                if x[0:4]=='FFF-':
                    daftarfile.append(x[4:])
            return self.create_return_message('200',daftarfile)
        except:
            return self.create_return_message('500','Error')

    def create(self, name='filename000'):
        nama='FFF-{}' . format(name)
        dirs = os.path.join(self.__get_storage_path(), nama)
        print("create ops {}" . format(dirs))
        try:
            if os.path.exists(dirs):
                return self.create_return_message('102', 'OK','File Exists')
            f = open(dirs,'wb',buffering=0)
            f.close()
            return self.create_return_message('100','OK')
        except:
            return self.create_return_message('500','Error')
    def read(self,name='filename000'):
        nama='FFF-{}' . format(name)
        dirs = os.path.join(self.__get_storage_path(), nama)
        print("read ops {}" . format(dirs))
        try:
            f = open(dirs,'r+b')
            contents = f.read().decode()
            f.close()
            return self.create_return_message('101','OK',contents)
        except:
            return self.create_return_message('500','Error')
    def update(self,name='filename000',content=''):
        nama='FFF-{}' . format(name)
        dirs = os.path.join(self.__get_storage_path(), nama)
        print("update ops {}" . format(dirs))

        if (str(type(content))=="<class 'dict'>"):
            content = content['data']
        try:
            f = open(dirs,'w+b')
            f.write(content.encode())
            f.close()
            return self.create_return_message('101','OK')
        except Exception as e:
            return self.create_return_message('500','Error',str(e))

    def delete(self,name='filename000'):
        nama='FFF-{}' . format(name)
        dirs = os.path.join(self.__get_storage_path(), nama)
        print("delete ops {}" . format(dirs))

        try:
            os.remove(dirs)
            return self.create_return_message('101','OK')
        except:
            return self.create_return_message('500','Error')

    def __root_folder_exists(self, root):
        if not os.path.exists(root):
            os.makedirs(root)

    def __get_storage_path(self) -> str:
        root = os.path.dirname(os.path.abspath(__file__)) + "/storage"
        self.__root_folder_exists(root)
        return root


if __name__ == '__main__':
    k = FileServer()
    print(k.create('f2'))
    print(k.update('f2',content='wedusku'))
    print(k.read('f2'))
    print(k.list())

