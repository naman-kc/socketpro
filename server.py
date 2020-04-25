import socket
import threading
import pickle
from keyExchange import *



port= 9951
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
    global out
    global Key
    print(f"[New Connection] {addr} requesting..")
    Obj = Diffi()
    SecretKey = int(input("Enter your SecreteKey: "))
    Exchange = Obj.diffi_KeySEND(SecretKey)
    print("Waiting for recever Exchange key.. .. ..")
    reqs = {1:"Press y for connection and n for reject..!", 2:Exchange}
    conn.send(pickle.dumps(reqs))
    Mess = pickle.loads(conn.recv(1024))
    #print(Mess[1])
    #print(Mess[2])

    #finding key:
    Exchange = int(Mess[2])
    Key = Obj.diffi_KeyGET(SecretKey, Exchange)

    ##################

    if Mess[1] == 'y':
        #thread = threading.Thread(target=handle_client,args=(conn,addr))
        #thread.start()
        handle_client(conn,addr)
    else:
        print("Connection request is rejected...!")
        out=False
        conn.close()
    



#handling client:..
def handle_client(conn,addr):
    global f
    global Key
    global out
    Obj1 = Enc_Dec()
    print(f"[Connection]:{addr[0]} connected..")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        if msg_length:
            msg= conn.recv(msg_length).decode(FORMAT)
            if msg == "X":
                connected = False
                out=False
                print("Connection Ended..!")
                break
            msg = Obj1.decrypt(msg,Key)
            if connected:
                print(f"[{addr[0]}]: {msg}")
    conn.close()
    f=0



# Start() method..
def start():

    global server
    global out
    server.listen(5)
    out = True
    while out:
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







