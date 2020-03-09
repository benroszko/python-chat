from socket import AF_INET, socket, SOCK_STREAM, SOCK_DGRAM
from threading import Thread

HOST = 'localhost'
TCP_PORT = 1234
UDP_PORT = 1235
TCP_ADDRESS = (HOST, TCP_PORT)
UDP_ADDRESS = (HOST, UDP_PORT)
BUFF_SIZE = 1024
SEPARATOR = ":::"
QUIT = ":q"


def expect_new_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has just connected." % client_address)
        client.send(bytes(
            "Hello in the ChatApp! Please, enter your name, then start chatting!",
            "utf8"))
        Thread(target=handle_one_connection, args=(
            client, client_address,)).start()


def handle_quit_msg(client):
    client.send(bytes(QUIT, "utf8"))
    client.close()
    del clients[client]


def handle_udp(client, client_name):
    print("START UDP")
    while True:
        msg, addr = SERVER_UDP.recvfrom(BUFF_SIZE)
        send2AllUDP(client, msg, client_name+": ")


def handle_one_connection(client, client_address):
    entered_name, udp_port = client.recv(
        BUFF_SIZE).decode("utf8").split(SEPARATOR)
    clients[client] = int(udp_port)
    send2All(client, bytes(entered_name + " has just joined the chat!", "utf8"))

    udp_th = Thread(target=handle_udp, args=(
        client, entered_name))
    udp_th.start()

    while True:
        msg = client.recv(BUFF_SIZE)
        if msg != bytes(QUIT, "utf8"):
            send2All(client, msg, entered_name+": ")
        else:
            handle_quit_msg(client)
            send2All(client, bytes(entered_name +
                                   " has left the chat.", "utf8"))
            print("%s:%s has just ended connection." % client_address)
            break


def send2All(client, msg, prefix=""):
    for sock in clients:
        if sock != client:
            sock.send(bytes(prefix, "utf8")+msg)


def send2AllUDP(client, msg, prefix=""):
    for sock in clients:
        if sock != client:
            SERVER_UDP.sendto(bytes(prefix, "utf8")+msg+bytes(' (UDP)', 'utf8'),
                              ('localhost', clients[sock]))


clients = {}

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER_UDP = socket(AF_INET, SOCK_DGRAM)
SERVER.bind(TCP_ADDRESS)
SERVER_UDP.bind(UDP_ADDRESS)

if __name__ == "__main__":
    SERVER.listen(100)
    print("Server is running on port %d..." % TCP_PORT)
    wati_for_connections_th = Thread(target=expect_new_connections)
    wati_for_connections_th.start()
    wati_for_connections_th.join()
    SERVER.close()
