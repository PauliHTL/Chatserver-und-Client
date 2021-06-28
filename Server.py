

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread



clients  = {}
addresses = {}
HOST = '127.0.0.1'
PORT = 5545
BUFFSIZE = 1024
ADDR = (HOST,PORT)
SERVER = socket(AF_INET,SOCK_STREAM)
SERVER.bind(ADDR)



def einkommende_Verbindungen():
    while True:
        client, clientAddress = SERVER.accept()
        print("%s:%s hat sich verbunden." % clientAddress)
        client.send(bytes("Hallo, bitte geben Sie Ihren Namen ein", "utf8"))
        addresses[client] = clientAddress
        Thread(target=clients_verwalten, args=(client,)).start()



def clients_verwalten(client):
    name = client.recv(BUFFSIZE).decode("utf8")
    client.send(bytes("Willkommen %s" % name,'utf8'))
    msg = '%s ist dem Chat beigetreten' % name
    broadcast(bytes(msg, 'utf8'))
    clients[client] = name
    while True:
        msg = client.recv(BUFFSIZE)
        if msg != bytes("'exit'", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("'exit'", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s hat den chat verlassen." % name, "utf8"))
            break



def broadcast(msg,prefix = ""):
    for client in clients:
        client.send(bytes(prefix,'utf8')+msg)


if __name__ == "__main__":
    SERVER.listen(5)
    print("Auf Verbindung warten...")
    ACCEPT_THREAD = Thread(target=einkommende_Verbindungen)
    ACCEPT_THREAD.start() 
    ACCEPT_THREAD.join()
    SERVER.close()