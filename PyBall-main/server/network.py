import socket
import pickle


class Network:
    # OBJECTIVE 3.1 - CREATING A NETWORK CLASS TO HANDLE ALL NETWORKING 
    def __init__(self,serverIp,port,initialData):
        # sets up the socket and connects to the server
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverIp = serverIp
        self.port = 5555
        self.address = (self.serverIp, self.port)
        # sets up the initial data, which is the data that is sent from the server when the client connects
        self.initialData = self.initialConnect(initialData)
        print(self.initialData)

    def getInitData(self):
        return self.initialData

    def initialConnect(self,data):
        # connects to the server and sends the initial data
        try:
            
            self.client.connect(self.address)
            self.client.send(pickle.dumps(data))
            
            return pickle.loads(self.client.recv(4096))
        except:
            pass

    def sendData(self, data):
        # sends data to the server
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(4096))
        except socket.error as e:
            print(e)
    def close(self):
        self.client.close()




def get_ip():
        tempSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        tempSocket.settimeout(0)
        try:
            #connect to dummy server to get ip
            tempSocket.connect(('8.8.8.8', 1))
            ip = tempSocket.getsockname()[0]
        except Exception:
            #if connection fails, most likely because linux shenanigans, use 127.0.0.1
            ip = '127.0.0.1'
        finally:
            tempSocket.close()
        return ip
    