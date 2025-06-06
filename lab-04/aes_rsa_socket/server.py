from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import socket
import threading

# Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)

# RSA key for the server
server_key = RSA.generate(2048)

# List to hold clients and their AES keys
clients = []

# Encrypt a message using AES
def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + ciphertext

# Decrypt a message using AES
def decrypt_message(key, encrypted_message):
    iv = encrypted_message[:AES.block_size]
    ciphertext = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_message.decode()

# Handle communication with a client
def handle_client(client_socket, client_address):
    print(f"[+] Connected with {client_address}")
    try:
        # Send server's public RSA key
        client_socket.send(server_key.publickey().export_key(format='PEM'))

        # Receive client's public RSA key
        client_received_key = RSA.import_key(client_socket.recv(2048))

        # Generate and encrypt AES key
        aes_key = get_random_bytes(16)
        cipher_rsa = PKCS1_OAEP.new(client_received_key)
        encrypted_aes_key = cipher_rsa.encrypt(aes_key)
        client_socket.send(encrypted_aes_key)

        # Store the client socket and AES key
        clients.append((client_socket, aes_key))

        # Listen for messages
        while True:
            encrypted_msg = client_socket.recv(1024)
            if not encrypted_msg:
                break

            decrypted_msg = decrypt_message(aes_key, encrypted_msg)
            print(f"[{client_address}] {decrypted_msg}")

            if decrypted_msg == "exit":
                break

            # Broadcast to other clients
            for client, key in clients:
                if client != client_socket:
                    try:
                        encrypted_broadcast = encrypt_message(key, decrypted_msg)
                        client.send(encrypted_broadcast)
                    except:
                        pass  # handle broken connections

    except Exception as e:
        print(f"[!] Error with client {client_address}: {e}")
    finally:
        print(f"[-] Disconnected: {client_address}")
        client_socket.close()
        clients.remove((client_socket, aes_key))

# Accept clients
print("[*] Server listening on port 12345...")
while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
