import random
import hashlib

# Large prime number (p) and primitive root (g)
p = 4096  # Example small prime number
g = 125   # Example small primitive root modulo p

def generate_private_key(p):
    return random.randint(2, p-2)

def generate_public_key(private_key, g, p):
    return pow(g, private_key, p)

def compute_shared_secret(received_public_key, private_key, p):
    return pow(received_public_key, private_key, p)

# Alice generates her private and public keys
alice_private_key = generate_private_key(p)
alice_public_key = generate_public_key(alice_private_key, g, p)

# Bob generates his private and public keys
bob_private_key = generate_private_key(p)
bob_public_key = generate_public_key(bob_private_key, g, p)

# Alice and Bob exchange public keys and compute the shared secret
alice_shared_secret = compute_shared_secret(bob_public_key, alice_private_key, p)
bob_shared_secret = compute_shared_secret(alice_public_key, bob_private_key, p)

# Verify that both shared secrets are the same
assert alice_shared_secret == bob_shared_secret

# Optionally, hash the shared secret for use as a symmetric key
shared_secret_hash = hashlib.sha256(str(alice_shared_secret).encode()).hexdigest()

print(f"Alice's Public Key: {alice_public_key}")
print(f"Bob's Public Key: {bob_public_key}")
print(f"Shared Secret: {alice_shared_secret}")
print(f"Hashed Shared Secret: {shared_secret_hash}")

