import socket
import threading
import sys
import os

# Cryptography Imports
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Configuration
HOST = '127.0.0.1'
PORT = 5555

class CryptoManager:
    """
    Handles Key Exchange (ECDH) and Encryption/Decryption (AES-GCM).
    """
    def __init__(self):
        # 1. Generate Ephemeral Elliptic Curve Key Pair (SECP256R1)
        self.private_key = ec.generate_private_key(ec.SECP256R1())
        self.public_key = self.private_key.public_key()
        self.shared_key = None
        self.aes_gcm = None

    def get_public_bytes(self):
        """Serialize public key to send to peer."""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def generate_shared_secret(self, peer_public_bytes):
        """
        Derive shared AES key from Peer's Public Key + My Private Key.
        """
        try:
            # Load peer's public key
            peer_public_key = serialization.load_pem_public_key(peer_public_bytes)
            
            # Perform ECDH
            shared_secret = self.private_key.exchange(ec.ECDH(), peer_public_key)
            
            # Derive a strong 256-bit AES key using HKDF
            derived_key = HKDF(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'handshake_salt_123', 
                info=b'handshake_data',
            ).derive(shared_secret)

            self.shared_key = derived_key
            self.aes_gcm = AESGCM(derived_key)
            return True
        except Exception as e:
            print(f"Crypto Error: {e}")
            return False

    def encrypt_message(self, plaintext):
        if not self.aes_gcm:
            return None
        
        # Generate a unique nonce (IV) for every message (12 bytes for GCM)
        nonce = os.urandom(12)
        ciphertext = self.aes_gcm.encrypt(nonce, plaintext.encode('utf-8'), None)
        return nonce + ciphertext # Prepend nonce for decryption

    def decrypt_message(self, payload):
        if not self.aes_gcm:
            return None
        
        try:
            # Extract nonce and actual ciphertext
            nonce = payload[:12]
            ciphertext = payload[12:]
            plaintext = self.aes_gcm.decrypt(nonce, ciphertext, None)
            return plaintext.decode('utf-8')
        except Exception:
            return "[Decryption Failed - Integrity Check Error]"

class Client:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((host, port))
        except ConnectionRefusedError:
            print("Could not connect to server. Is it running?")
            sys.exit()

        self.crypto = CryptoManager()
        self.handshake_complete = False

    def handshake(self):
        """
        Exchanges public keys to establish a shared secret (E2EE).
        """
        print("[*] Generating Keys...")
        my_pub_key = self.crypto.get_public_bytes()
        
        # Send my public key header
        header = b'KEY_EXCHANGE:'
        self.client.send(header + my_pub_key)
        print("[*] Public Key Sent. Waiting for peer...")

    def receive_messages(self):
        while True:
            try:
                data = self.client.recv(4096)
                if not data:
                    break

                # Check if it's a handshake Key
                if data.startswith(b'KEY_EXCHANGE:'):
                    if not self.handshake_complete:
                        peer_key_bytes = data[13:] # Strip header
                        success = self.crypto.generate_shared_secret(peer_key_bytes)
                        if success:
                            print("\n[SUCCESS] Secure Channel Established!")
                            print(f"[INFO] AES-256-GCM Session Key Derived.")
                            print("-----------------------------------------")
                            self.handshake_complete = True
                            
                            # CRITICAL FIX: Resend my public key to the peer.
                            # If the peer joined late (Client B), they missed my first broadcast.
                            # Sending it again now ensures they can also complete the handshake.
                            response_key = b'KEY_EXCHANGE:' + self.crypto.get_public_bytes()
                            self.client.send(response_key)
                        else:
                            print("[ERROR] Key Exchange Failed.")
                    else:
                        pass # Ignore extra keys if we are already secure
                
                # Normal Encrypted Message
                else:
                    if self.handshake_complete:
                        decrypted = self.crypto.decrypt_message(data)
                        print(f"\rPeer: {decrypted}\nYou: ", end="", flush=True)
                    else:
                        print("\n[!] Received data before handshake complete.")

            except Exception as e:
                print(f"\n[!] Connection Error: {e}")
                self.client.close()
                break

    def send_messages(self):
        # Initial Handshake trigger
        self.handshake()
        
        while True:
            msg = input("You: ")
            if self.handshake_complete:
                encrypted_payload = self.crypto.encrypt_message(msg)
                if encrypted_payload:
                    self.client.send(encrypted_payload)
            else:
                print("[!] Waiting for secure connection...")

    def start(self):
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

        self.send_messages()

if __name__ == "__main__":
    print("=== End-to-End Encrypted Chat Client ===")
    client = Client(HOST, PORT)
    client.start()