import socket
import ssl

DESTINATION_IP = '127.0.0.1'
DESTINATION_PORT = 7777

ssl_context = ssl.create_default_context()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket_ssl = ssl_context.wrap_socket(client_socket, server_hostname='localhost')

client_socket_ssl.connect((DESTINATION_IP, DESTINATION_PORT))

client_socket_ssl.send("hello from the client".encode())

data = client_socket_ssl.recv(1024)
print(f"Received: {data.decode('utf-8')}")

client_socket_ssl.close()