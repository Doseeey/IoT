from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import socket
import time

# Generate RSA key pair for the client
# private_key_client = rsa.generate_private_key(
#     public_exponent=65537,
#     key_size=2048,
#     backend=default_backend()
# )
# public_key_client = private_key_client.public_key()
start = time.time()
# Client setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

# Receive server public key
server_public_key_pem = client_socket.recv(4096)

# Deserialize server public key
server_public_key = serialization.load_pem_public_key(
    server_public_key_pem,
    backend=default_backend()
)
print(f"Recieved server public key:\n")
for line in server_public_key_pem.splitlines():
    print(f"{line}")
# Send encrypted message to server
def send_message(message_size):
    message = "d" * message_size
    encrypted_message = server_public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    client_socket.sendall(encrypted_message)
    print("Message sent to server:", message)
    #print("Message sent to server after encryption: ", encrypted_message)

# for i in range(10):
#     send_message(64*(i+1))

send_message(10)
end = time.time()
print(f"Sending time: {end-start}")

# Close socket
client_socket.close()
