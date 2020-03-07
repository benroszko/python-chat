from socket import AF_INET, socket, SOCK_STREAM, SOCK_DGRAM
from threading import Thread

HOST = 'localhost'
PORT = 1234
BUFF_SIZE = 1024
ADDRESS = (HOST, PORT)
QUIT = ":q"


def expect_new_connections():
    while True:
        client, client_address = SERVER.accept()
        clients.append(client)
        print("%s:%s has just connected." % client_address)
        client.send(bytes(
            "Hello in the ChatApp! Please, enter your name, then start chatting!",
            "utf8"))
        Thread(target=handle_one_connection, args=(
            client, client_address,)).start()


def handle_quit_msg(client):
    client.send(bytes(QUIT, "utf8"))
    client.close()
    clients.remove(client)


def handle_udp(client, client_address, client_name):
    print("START UDP")
    while True:
        msg = client.recvfrom(BUFF_SIZE)[0]
        print("GOTIT")
        send2AllUDP(client, client_address, msg, client_name+": ")


def handle_one_connection(client, client_address):
    entered_name = client.recv(BUFF_SIZE).decode("utf8")
    send2All(client, bytes(entered_name + " has just joined the chat!", "utf8"))

    udp_th = Thread(target=handle_udp, args=(
        client, client_address, entered_name))
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
            udp_th.exit()
            break


def send2All(client, msg, prefix=""):
    for sock in clients:
        if sock != client:
            sock.send(bytes(prefix, "utf8")+msg)


def send2AllUDP(client, client_address, msg, prefix=""):
    for sock in clients:
        if sock != client:
            sock.sendto(prefix.encode()+msg, client_address)


clients = []

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER_UDP = socket(AF_INET, SOCK_DGRAM)
SERVER.bind(ADDRESS)
SERVER_UDP.bind(ADDRESS)

if __name__ == "__main__":
    SERVER.listen(100)
    print("Server is running on port %d..." % PORT)
    wati_for_connections_th = Thread(target=expect_new_connections)
    wati_for_connections_th.start()
    wati_for_connections_th.join()
    SERVER.close()
