from flup.server.fcgi import WSGIServer 
from main import app 
if __name__ == '__main__': 
    #help (WSGIServer) 
    WSGIServer(app,multithreaded=1, multiprocess=0, 
               debug=1 , 
               bindAddress=('127.0.0.1',8080)).run() 
