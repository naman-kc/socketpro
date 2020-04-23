import socket
import threading
import pickle
from keyExchange import *

key=0
f=0
port= 5051
host = socket.gethostbyname(socket.gethostname())
ADDR = (host,port)
FORMAT = 'utf-8'
HEADER= 64


# Create a Socket
def create_socket():
    try:
        global server
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global server
        print("Binding the Port: " + str(port))
        server.bind(ADDR)


    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()



#request..
def Request(conn,addr):

    global key
    print(f"[New Connection] {addr} requesting..")
    Obj = Diffi()
    SecretKey = 6
    Exchange = Obj.diffi_KeySEND(SecretKey)
    reqs = {1:"Press y for connection and n for reject..!", 2:Exchange}
    conn.send(pickle.dumps(reqs))
    Mess = pickle.loads(conn.recv(1024))
    print(Mess[1])
    print(Mess[2])

    #finding key:
    Exchange = int(Mess[2])
    Key = Obj.diffi_KeyGET(SecretKey, Exchange)
    ##################

    if Mess[1] == 'y':
        thread = threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()
    else:
        print("Connection request is rejected...!")
        conn.close()
    



#handling client:..
def handle_client(conn,addr):
    
    global key
    #Obj = Enc_Dec()
    print(f"[Connection]:{addr[0]} connected..")
    connected = True
    while connected:
        # try:
        #     msg_length = conn.recv(HEADER).decode(FORMAT)
        #     msg_length = int(msg_length)
        # except:
        #     print("error is here..!")
        # if msg_length:
            
        #     msg= conn.recv(msg_length).decode(FORMAT)
            #msg = Obj.decrypt(msg, key)
        msg = pickle.loads(conn.recv(1024))
        if msg == "X":
            connected = False
            # msg= conn.recv(msg_length).decode(FORMAT)
            # print(f"[{addr[0]}]: {msg}")
        print(f"[{addr[0]}]: {msg}")
    conn.close()



# Start() method..
def start():

    global server
    global f
    server.listen(5)

    while True:
        conn, addr= server.accept()
        #print(f"[Active connections..]{threading.activeCount()-1}")
        Request(conn,addr) 
        conn.close()   


def main():
    create_socket()
    bind_socket()
    print("[Starting] server is starting..")
    start()
    
   

main()







