End-to-End Encrypted Chat Relay 🔒

A secure, multi-threaded P2P messaging system built with Python. This project demonstrates true End-to-End Encryption (E2EE) using Elliptic Curve Cryptography and AES-GCM, ensuring that the relay server remains completely blind to the message content.

🚀 Features

True End-to-End Encryption: Messages are encrypted locally on the client before transmission. The server only sees encrypted bytes.

Perfect Forward Secrecy: Uses Ephemeral Elliptic Curve Diffie-Hellman (SECP256R1) keys. Keys are generated fresh for every session and are never stored.

Authenticated Encryption: Implements AES-256-GCM to provide both confidentiality and integrity. Any tampering with the ciphertext is immediately detected.

Blind Relay Architecture: The server acts as a dumb pipe, broadcasting raw bytes without the ability to decrypt them.

Multi-threaded Client: Handles sending and receiving messages simultaneously for a seamless chat experience.

🛠️ Technology Stack

Language: Python 3

Networking: socket, threading

Cryptography: cryptography library (hazmat primitives)

Key Exchange: ECDH (SECP256R1)

KDF: HKDF (SHA-256)

Encryption: AES-GCM (256-bit)

📋 Prerequisites

You need Python 3 installed. You also need to install the cryptography library:
pip install cryptography

⚙️ How to Run

This system requires one server instance and at least two client instances.

1. Start the Server

Open a terminal and run the server. It will listen for incoming connections.

python secure_server.py


2. Start Client A

Open a new terminal window and run the client.

python secure_client.py


3. Start Client B

Open a third terminal window and run the client.

python secure_client.py


Once the second client joins, the cryptographic handshake will occur automatically. You will see [SUCCESS] Secure Channel Established! on both screens. You can now chat securely!

🔐 Security Architecture

Connection: Clients connect to the central relay server via TCP sockets.

Handshake (ECDH):

On startup, each client generates an ephemeral private/public key pair.

Clients exchange public keys via the server.

Each client mathematically derives the same shared secret using their private key and the peer's public key.

Key Derivation: The shared secret is passed through HKDF (HMAC-based Key Derivation Function) to generate a strong 256-bit AES session key.

Transport:

Messages are encrypted using AES-256-GCM.

A unique nonce (IV) is generated for every message.

The ciphertext + nonce are sent to the server.

The server broadcasts the payload to the other client.

The recipient verifies the integrity tag and decrypts the message.

⚠️ Disclaimer

This project is for educational purposes to demonstrate cryptographic concepts and socket programming. While it uses industry-standard algorithms, it lacks features required for a production-grade secure messenger (e.g., identity verification/signing to prevent Man-in-the-Middle attacks between the client and server during the initial handshake).

📄 License

This project is open-source. Feel free to use it for learning or as a base for your own projects.
