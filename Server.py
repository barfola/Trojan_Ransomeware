import socket
import ssl
import threading

SERVER_IP = '127.0.0.1'
SERVER_PORT = 7777


def wrap_socket_with_ssl_layer(socket_obj: socket.socket):
    """
    :param socket_obj: socket object
    :return server_socket_ssl:
    :return type: socket object
    :Description: this function will wrap regular socket with ssl layer
    for enhanced security. ssl_context is managing the setting of the ssl socket.
    the "server.crt" is the certificate that I created for the server in order
    to expose his identity to the client, also contains the public encryption key.
    the "server.key" contains the decryption key.
    """
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile='server.crt', keyfile='server.key')
    server_socket_ssl = ssl_context.wrap_socket(socket_obj, server_side=True)

    return server_socket_ssl


def handle_client(client_socket: socket.socket, client_address):
    print(f"New connection from {client_address}")
    client_socket.send("Hello from the server".encode())


def start_server(server_port, server_ip='127.0.0.1', waiting_list_size=1):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(waiting_list_size)

    server_socket_ssl = wrap_socket_with_ssl_layer(server_socket)

    print("Server is up and running on [127.0.0.1:7777]")

    while True:
        client_socket, client_address = server_socket_ssl.accept()

        client_handler_thread = threading.Thread(target=handle_client, args=(client_socket, server_socket_ssl))
        client_handler_thread.start()


start_server(server_port=SERVER_PORT, server_ip=SERVER_IP, waiting_list_size=3)
