import socket
import ssl

SERVER_IP = '127.0.0.1'
SERVER_PORT = 7777

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile='server.crt', keyfile='server.key')

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(1)

server_socket_ssl = ssl_context.wrap_socket(server_socket, server_side=True)

print(f"Server is up on {SERVER_PORT}")

while True:
    client_socket, addr = server_socket_ssl.accept()
    print(f"Connection established with {addr}")

    data = client_socket.recv(1024)
    print(f"Received: {data.decode()}")

    client_socket.send(b"Hello from the server!")

    client_socket.close()