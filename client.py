import tkinter
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

"""
The below function gets the latest messages from the server and inserts it into the Listbox object.
If the window has somehow been closed abruptly, we remove the user.
"""
def receive():
    stop = False
    while True and not stop:
        try:
            msg = clientSocket.recv(BUFFSIZE).decode('utf8')
            msgList.insert(tkinter.END,msg)
        except OSError:
            cleanAndClose()
            break

"""
The below function sends the messages of the user to the server to be broadcast, 
if the exit sequence is entered, user's data is purged, and the window is closed.
"""
def send(event=None):
    msg = myMsg.get()
    myMsg.set("")
    clientSocket.send(bytes(msg,'utf8'))

def cleanAndClose(event=None):
    myMsg.set("'exit'")
    send()
    top.destroy()
    stop = True

def Resize_Image(image, maxsize):
    r1 = tk.image.size[0]/maxsize[0]
    r2 = tk.image.size[1]/maxsize[1]
    ratio = max(r1, r2)
    newsize = (int(tk.image.size[0]/ratio), int(tk.image.size[1]/ratio))
    image = tk.image.resize(newsize, tk.Image.ANTIALIAS)
    return image

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
    myMsg.set("Klicken, um zu schreiben")
    entryField = tkinter.Entry(top,textvariable = myMsg)
    entryField.bind("<Return>", send)
    entryField.pack()

    sendimg=tkinter.PhotoImage('send-button.png')
    Resize_Image(sendimg, 400)
    sendButton = tkinter.Button(top, image = sendimg, command = send)





    leaveButton = tkinter.Button(top, text='Verlassen', command = cleanAndClose, height = 1, width = 7)
    sendButton.pack()
    leaveButton.pack()

    top.protocol("WM_DELETE_WINDOW", cleanAndClose)

    HOST = input('Geben Sie die HOST-Adresse ein: ')
    PORT = input('Geben Sie die PORT-Nummer ein: ')
    PORT = 5545 if not PORT else int(PORT)

    BUFFSIZE = 1024
    ADDR = (HOST, PORT)
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(ADDR)

    receiveThread = Thread(target=receive)
    receiveThread.start()
    tkinter.mainloop()  
    receiveThread.join()