import socket
import pickle
from keyExchange import *

f=0
key=0
port= 9951
host =socket.gethostbyname(socket.gethostname())
ADDR = (host,port)
FORMAT = 'utf-8'
HEADER= 64

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect(ADDR)

def Request():
    global f
    global key
    Obj = Diffi()
    print("Waiting for recever Exchange key.. .. ..")
    req = pickle.loads(client.recv(1024))
    print(req[1])
    entry = input()
    SecretKey = int(input("Enter your Secret Key: "))
    Exchange = Obj.diffi_KeySEND(SecretKey)
    key = Obj.diffi_KeyGET(SecretKey, req[2])
    reply = {1:entry,2:Exchange}
    client.send(pickle.dumps(reply))
    
    if reply[1] == 'n':
        print("Connection request is rejected")
        client.close()
        f = 1



def send():
    
    connected = True

    while connected:
        string =input(str("enter the message or enter X for end the message: "))
        if string == 'X':
            connected = False
            msg="X"
            message = msg.encode(FORMAT)
            msg_length = len(string)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' '*(HEADER-len(send_length))
            client.send(send_length)
            client.send(message)
            #client.send(pickle.dumps(msg))
            print("Connection Ended..!")
            break
        Obj = Enc_Dec()
        msg = Obj.encrypt(string, key)
        print("encrypted msg: "+msg)
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' '*(HEADER-len(send_length))
        client.send(send_length)
        client.send(message)
        #client.send(pickle.dumps(msg))


Request()
if f != 1:
    send()





