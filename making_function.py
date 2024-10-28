import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


def encrypt_file_with_aes(file_path, aes_encryption_key):
    with open(file_path, 'rb') as file:
        file_data = file.read()

    initialization_vector = get_random_bytes(16)

    cipher = AES.new(aes_encryption_key, AES.MODE_CBC, initialization_vector)
    encrypted_data = cipher.encrypt(pad(file_data, AES.block_size))

    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(initialization_vector + encrypted_data)


def decrypt_file_with_aes(encrypted_file_path, aes_decryption_key):
    with open(encrypted_file_path, 'rb') as encrypted_file:
        initialization_vector = encrypted_file.read(16)

        encrypted_data = encrypted_file.read()

    cipher = AES.new(aes_decryption_key, AES.MODE_CBC, initialization_vector)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

    with open(encrypted_file_path, "wb") as decrypted_file:
        decrypted_file.write(decrypted_data)


def encrypt_files(starting_directory):
    for directory_path, sub_directories_names, file_names in os.walk(starting_directory):
        pass


iv = get_random_bytes(16)
aes_encryption_key = os.urandom(32)
encrypt_file_with_aes("try_to_encrypt.txt", aes_encryption_key)
#decrypt_file_with_aes("try_to_encrypt.txt", aes_encryption_key)
