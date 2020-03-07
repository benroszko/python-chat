from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

HOST = 'localhost'
PORT = 1234
BUFF_SIZE = 1024
ADDRESS = (HOST, PORT)
QUIT = ":q"


def expect_new_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has just connected." % client_address)
        client.send(bytes(
            "Hello in the ChatApp! Please, enter your name, then start chatting!", "utf8"))
        Thread(target=handle_one_connection, args=(
            client, client_address,)).start()


def handle_one_connection(client, client_address):
    entered_name = client.recv(BUFF_SIZE).decode("utf8")
    clients.append(client)
    send2All(bytes(entered_name + " has just joined the chat!", "utf8"))

    while True:
        msg = client.recv(BUFF_SIZE)
        if msg != bytes(QUIT, "utf8"):
            send2All(msg, entered_name+": ")
        else:
            client.send(bytes(QUIT, "utf8"))
            client.close()
            clients.remove(client)
            send2All(bytes(entered_name +
                           " has left the chat.", "utf8"))
            print("%s:%s has just ended connection." % client_address)
            break


def send2All(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


clients = []

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDRESS)

if __name__ == "__main__":
    SERVER.listen(100)
    print("Server is running on port %d..." % PORT)
    wati_for_connections_th = Thread(target=expect_new_connections)
    wati_for_connections_th.start()
    wati_for_connections_th.join()
    SERVER.close()
