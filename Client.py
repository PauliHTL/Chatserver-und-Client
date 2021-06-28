from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter



def receive():
    stop = False
    while True and not stop:
        try:
            msg = clientSocket.recv(BUFFSIZE).decode('utf8')
            msgList.insert(tkinter.END,msg)
        except OSError:
            cleanAndClose()
            break


def send(event=None):
    msg = myMsg.get()
    myMsg.set("")
    clientSocket.send(bytes(msg,'utf8'))
    if msg is "'exit'":
        clientSocket.close()
        cleanAndClose()
        top.quit()


def cleanAndClose(event=None):
    myMsg.set("'exit'")
    send()
    top.destroy()
    stop = True

if __name__ == '__main__':
    top = tkinter.Tk()
    top.title('ChatRoom')
    messageFrame = tkinter.Frame(top)
    scrollbar = tkinter.Scrollbar(messageFrame)

    msgList = tkinter.Listbox(messageFrame, width = 50, yscrollcommand = scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msgList.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msgList.pack(fill = tkinter.X)
    messageFrame.pack()

    myMsg = tkinter.StringVar()
    myMsg.set("Click to type")
    entryField = tkinter.Entry(top,textvariable = myMsg)
    entryField.bind("<Return>", send)
    entryField.pack()
    bildsende = tkinter.PhotoImage(file='Bild1.png')
    sendButton = tkinter.Button(top, command = send, image=bildsende)
    sendButton.pack()
    leaveButton = tkinter.Button(top, text='exit', command=cleanAndClose, height=1, width=5)
    leaveButton.pack()

    top.protocol("WM_DELETE_WINDOW", cleanAndClose)

    HOST = input('Host Adresse eingeben: ')
    PORT = input('Port Nummer eingeben: ')
    PORT = 5545 if not PORT else int(PORT)

    BUFFSIZE = 1024
    ADDR = (HOST, PORT)
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(ADDR)

    receiveThread = Thread(target=receive)
    receiveThread.start()
    tkinter.mainloop()
    receiveThread.join()