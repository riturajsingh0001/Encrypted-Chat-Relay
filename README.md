End-to-End Encrypted Chat Relay 🔒

A robust, multi-threaded P2P messaging system built with Python. This project demonstrates true End-to-End Encryption (E2EE) using Elliptic Curve Cryptography and AES-GCM.

The core philosophy of this project is a "Blind Relay" architecture: the server routes data between clients but possesses mathematically zero capability to decrypt or read the messages it handles.

🚀 Key Features

True End-to-End Encryption: Encryption happens entirely on the client-side. The server only sees and transmits encrypted binary data.

Perfect Forward Secrecy (PFS):

Uses Ephemeral Keys (SECP256R1).

A new private/public key pair is generated in RAM every time the script runs.

Even if a device is seized later, past conversations cannot be decrypted because the keys no longer exist.

Authenticated Encryption:

Implements AES-256-GCM (Galois/Counter Mode).

Provides both confidentiality (secrecy) and integrity (tamper-proofing).

If a packet is intercepted and a single bit is flipped, the decryption will fail immediately, alerting the user.

Zero-Knowledge Server: The relay server stores no logs, no databases, and no keys. It acts purely as a volatile RAM-based router.

Auto-Handshake Recovery: Smart handshake logic ensures clients can exchange keys reliably, regardless of join order (solving the "late joiner" problem).

🛠️ Technology Stack

Language: Python 3.x

Networking:

socket (Low-level TCP/IP communication)

threading (For simultaneous sending/receiving)

Cryptography: cryptography library (hazmat primitives)

Key Exchange: Elliptic Curve Diffie-Hellman (ECDH) using SECP256R1.

Key Derivation: HKDF (HMAC-based Key Derivation Function) with SHA-256.

Symmetric Encryption: AES-GCM (256-bit key size).

📋 Prerequisites

You need Python 3.6+ installed. You also need to install the cryptography library, which provides the low-level security primitives:

pip install cryptography


⚙️ How to Run

This system requires one server instance and two client instances.

1. Start the Relay Server

Open a terminal and run the server. It will bind to 127.0.0.1:5555 and listen for incoming TCP connections.

python secure_server.py


Output: [*] Server listening on 127.0.0.1:5555

2. Start Client A

Open a new terminal window and run the client.

python secure_client.py


Output: [*] Generating Keys... Public Key Sent. Waiting for peer...

3. Start Client B

Open a third terminal window and run the client.

python secure_client.py


As soon as the second client connects, they will automatically exchange public keys. You will see [SUCCESS] Secure Channel Established! on both screens. You can now chat securely!

🔐 Detailed Security Workflow (With Code)

Here is exactly what happens under the hood when you run the chat, mapping the logic to the actual Python code:

1. Initialization (Ephemeral Keys)

When the client starts, it generates a fresh Elliptic Curve key pair. These are "ephemeral," meaning they only exist in memory for this specific session.

# Generate private key (d) and public key (Q)
self.private_key = ec.generate_private_key(ec.SECP256R1())
self.public_key = self.private_key.public_key()


2. The Handshake (ECDH)

Clients exchange Public Keys via the server. The server acts as a bridge but cannot use these public keys to derive the secret. Once a client receives the peer's public bytes, it computes the shared secret.

# Compute Shared Secret (S) using My Private Key + Peer Public Key
shared_secret = self.private_key.exchange(ec.ECDH(), peer_public_key)


3. Key Hardening (HKDF)

The raw ECDH secret is not uniform enough to be used as an encryption key directly. We pass it through HKDF (SHA-256) to derive a cryptographically strong 256-bit Session Key.

# Derive 32-byte (256-bit) AES Key
derived_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=b'handshake_salt_123', 
    info=b'handshake_data',
).derive(shared_secret)


4. Authenticated Encryption (AES-GCM)

When sending a message, we generate a unique Nonce (Number Used Once). This ensures that even if you send the same message twice ("Hello", "Hello"), the encrypted output looks completely different.

# Encrypting "Hello"
aes_gcm = AESGCM(derived_key)
nonce = os.urandom(12) # Unique IV
ciphertext = aes_gcm.encrypt(nonce, b"Hello", None)

# The payload sent over the wire is:
final_packet = nonce + ciphertext 


5. Decryption & Integrity Check

The recipient splits the nonce and the ciphertext. AES-GCM automatically verifies the "Integrity Tag" (embedded in the ciphertext). If the message was tampered with during transit, this function throws an exception, and the message is rejected.

plaintext = aes_gcm.decrypt(nonce, ciphertext, None)


❓ Troubleshooting

"ConnectionRefusedError": The server is not running. Make sure you run secure_server.py first and keep that window open.

"[!] Received data before handshake complete": This is a timing issue where one client tries to decrypt a message before it has received the other person's key. Ensure both clients are connected and have seen the [SUCCESS] message before typing.

ModuleNotFoundError: No module named 'cryptography': You forgot to run pip install cryptography.

⚠️ Educational Disclaimer

This project is designed for educational purposes to demonstrate secure socket programming and cryptographic implementation details.

While it uses industry-standard algorithms, a production-grade secure messenger (like Signal/WhatsApp) requires additional layers:

Identity Keys: To verify who you are talking to (preventing active Man-in-the-Middle attacks where an attacker acts as the server).

Double Ratchet Algorithm: For rotating keys with every single message (Forward Secrecy at the message level).

📄 License

This project is open-source. Feel free to use it for learning, portfolios, or as a base for your own projects.
