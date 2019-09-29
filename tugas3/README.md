
### How
 - install dependencies `pip install -r requirements.txt`
 - run `pyro4-ns -n localhost -p 7777`
 - server `cd server && python greet_server.py`
 - client `cd client && python client.py`

### Available Commands
- `list` : get all files in server storage directory  \
  option : `-a` / `-all`\
  example : `list -a`
- `create` : make new file/files  
  syntax : `create file1 file2 file3`  \
  example : `create text.txt "lorem ipsum.py"`
- `delete` : delete file/files  
  syntax : `delete file1 file2 file3`  \
  example : `delete text.txt "lorem ipsum.py"`
- `read` : read file  
  syntax : `read file`  \
  example : `read text.txt`
- `update` : update file or create new file if not exists  
  option : `--append` / `-a`, `--overwrite` / `-o`\
  syntax : `update option file content`  \
  example : `update --append text.txt "lorem ipsumsit dolor amet"`
- `exit` : exit  
  syntax : `exit`  \
  example : `exit`