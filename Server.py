import socket
import os
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox
import threading as t
from pathlib import Path


# Variables
HEADER = 10
CHUNK_SIZE = 8 * 1024
s = socket.socket()
host = socket.gethostname()
port = 15562
filelist = []
s.bind((host, port))
s.listen(1)


# functions
def filePicker():
    global filelist
    filename1 = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(
        ("mp4 files", "*.mp4"), ("wmv files", "*.wmv"), ("all files", "*.*")))
    filelist.append(filename1)
    print(filename1)
    for file in filelist:
        fileFrame.delete(0, "end")
    for file in filelist:
        p = Path(file)
        fileFrame.insert("end", p.name)


def filenames():
    for file in filelist:
        p = Path(file)
        filedata = f'{len(p.name):<{HEADER}}' + p.name
        conn.send(bytes(filedata, "utf-8"))


def connectionchecker():
    global conn, addr
    conn, addr = s.accept()
    connectionlabel.config(fg='green')
    textVar.set("Connected!")


def startTransfer():
    filenames()
    # transferFile()


def transferFile():
    global filelist
    for file in filelist:
        file_size = os.path.getsize(file)
        with open(file, 'rb') as f:
            file_data = f.read(CHUNK_SIZE)
            while file_data:
                conn.send(file_data)
                file_data = f.read(CHUNK_SIZE)
        print(file)
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()
    s.close()

    tkinter.messagebox.showinfo('Transfer Successful',
                                'The File has been Transfered Successfully!')


connection = t.Thread(target=connectionchecker)
connection.start()

root = tk.Tk()
root.title('File Sender 3000')
root.minsize(width=1000, height=562)

# Connection text variable
textVar = tk.StringVar()
textVar.set("Waiting for Connection...")

# Frames
topframe = tk.Frame(root, bg='#0f0f0f')
sideframe = tk.Frame(root, bg='#0f0f0f', width=200)
mainframe = tk.Frame(root, bg='#000000')
topframe.pack(side=tk.TOP, fill=tk.X)
sideframe.pack(side=tk.LEFT, fill=tk.Y)
mainframe.pack(fill=tk.BOTH, expand=1)

# content
hostlabel = tk.Label(topframe, text=("Host Name: " + host), bg='#0f0f0f'
                     , fg='green', font=("Arial", 20)).pack(anchor=tk.NW, padx=15, pady=10)

connectionlabel = tk.Label(mainframe, textvariable=textVar
                           , bg='black', fg='red', font=("Arial", 12))
connectionlabel.grid(columnspan=5, padx=15, pady=15, sticky=tk.W)

filenametext = tk.Label(mainframe, bg='black', fg='white', font=("Arial", 12)
                        , text='Enter File Name:').grid(row=1, sticky=tk.W, padx=15, pady=15)

enterFileName = tk.Entry(mainframe, bg='black', fg='white')
enterFileName.grid(column=1, row=1, sticky=tk.W)

browse = tk.Button(mainframe, text='Browse...', bg='black', fg='white', command=filePicker).grid \
    (column=2, row=1, sticky=tk.W)

transferbutton = tk.Button(mainframe, text="Transfer File", command=startTransfer
                           , bg='#0f0f0f', fg='white', height=1).grid(column=1, row=2, sticky=tk.W)

fileFrame = tk.Listbox(mainframe, bg='#0f0f0f', fg='white', width=75, height=15)
fileFrame.grid(columnspan=5, row=3, sticky=tk.W, padx=20, pady=20)

root.mainloop()
