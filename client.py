from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

HOST = 'localhost'
PORT = 1234
BUFFSIZE = 1024
ADDRESS = (HOST, PORT)
QUIT = ':q'


def tk_insert_and_focus_on_last_msg(msg):
    msg_list.insert(tkinter.END, msg)
    msg_list.see(tkinter.END)


def send():
    msg = msg_var.get()
    msg_var.set('')
    if msg != '':
        client_tcp_socket.send(bytes(msg, "utf8"))
        if msg != QUIT:
            global client_name
            if client_name == '':
                client_name = msg
                tk.title("ChatApp - " + client_name)
            else:
                tk_insert_and_focus_on_last_msg('%s: %s' % (client_name, msg))
        else:
            client_tcp_socket.close()
            tk.quit()


def receive():
    while True:
        try:
            msg = client_tcp_socket.recv(BUFFSIZE).decode('utf8')
            tk_insert_and_focus_on_last_msg(msg)
        except OSError:
            break


def handle_closing_window():
    msg_var.set(QUIT)
    send()


tk = tkinter.Tk()
tk.title('ChatApp')
chat_field = tkinter.Frame(tk)
msg_var = tkinter.StringVar()
scroll = tkinter.Scrollbar(chat_field)
msg_list = tkinter.Listbox(chat_field, height=15,
                           width=50, yscrollcommand=scroll.set)
scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
chat_field.pack()
msg_field = tkinter.Entry(tk, textvariable=msg_var)
msg_field.bind("<Return>", send)
msg_field.pack()
send_btn = tkinter.Button(tk, text="Send", command=send)
send_btn.pack()
tk.protocol("WM_DELETE_WINDOW", handle_closing_window)

# CLIENT MAIN
client_name = ''
client_tcp_socket = socket(AF_INET, SOCK_STREAM)
client_tcp_socket.connect(ADDRESS)

receiving_th = Thread(target=receive)
receiving_th.start()
tkinter.mainloop()
