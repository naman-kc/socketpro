import socket
import pickle
from keyExchange import *

f=0
key=0
port= 5051
host = socket.gethostbyname(socket.gethostname())
ADDR = (host,port)
FORMAT = 'utf-8'
HEADER= 64

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect(ADDR)

def Request():
    global f
    global key
    Obj = Diffi()
    
    SecretKey = 15
    Exchange = Obj.diffi_KeySEND(SecretKey)
    req = pickle.loads(client.recv(1024))
    print(req[1])
    key = Obj.diffi_KeyGET(SecretKey, req[2])
    entry = input()
    reply = {1:entry,2:Exchange}
    client.send(pickle.dumps(reply))
    
    if reply[1] == 'n':
        print("Connection request is rejected")
        client.close()
        f = 1



def send(msg):
    
    connected = True
    
    while connected:
        # message = msg.encode(FORMAT)
        # msg_length = len(message)
        # send_length = str(msg_length).encode(FORMAT)
        # send_length += b' '*(HEADER-len(send_length))
        # client.send(send_length)
        # client.send(message)
        client.send(pickle.dumps(msg))
        a = input()
        if a == 'X':
            connected = False
            msg= "Connection Ended"
            # message = msg.encode(FORMAT)
            # msg_length = len(message)
            # send_length = str(msg_length).encode(FORMAT)
            # send_length += b' '*(HEADER-len(send_length))
            # client.send(send_length)
            # client.send(message)
            client.send(pickle.dumps(msg))
            print("Connection Ended..!")

Request()
if f != 1:
    string = "hello world!"
    Obj = Enc_Dec()
    msg = Obj.encrypt(string, key)
    print("encrypted msg: "+msg)
    send(msg)
#send("X")




