End-to-End Encrypted Chat Relay 🔒

A robust, multi-threaded P2P messaging system built with Python. This project implements true End-to-End Encryption (E2EE) using Elliptic Curve Cryptography and AES-GCM, ensuring a "blind" relay server architecture where the server cannot read message content.


🚀 Key Features

True E2EE: Encryption happens on the client-side; the server only routes encrypted bytes.

Perfect Forward Secrecy: Uses ephemeral ECDH (SECP256R1) keys, regenerated every session to protect past conversations.

Tamper-Proof Security: Implements AES-256-GCM for authenticated encryption, ensuring immediate detection of message tampering.

Blind Relay: Zero-knowledge server architecture—no logs, no storage, no decryption.

Real-time Communication: Multi-threaded client for simultaneous sending and receiving.


🛠️ Tech Stack

Language: Python 3

Networking: Raw Sockets & Threading

Cryptography: cryptography library

Exchange: ECDH (SECP256R1)

KDF: HKDF (SHA-256)

Cipher: AES-GCM (256-bit)


📋 Quick Start

1. Install Dependencies

pip install cryptography


2. Start the Server

python secure_server.py


3. Connect Clients
Open two new terminals and run the client script in each:

# Terminal 2 (Client A)
python secure_client.py

# Terminal 3 (Client B)
python secure_client.py


The secure handshake is automatic. You will see [SUCCESS] Secure Channel Established! once connected.


🔐 Security Architecture

Handshake: Clients perform an ECDH Key Exchange via the server to generate a shared secret without exposing it.

Derivation: The shared secret is salted and passed through HKDF (SHA-256) to derive a unique session key.

Transport: Messages are encrypted with AES-256-GCM using unique nonces, guaranteeing confidentiality and data integrity.


⚠️ Disclaimer

Designed for educational purposes to demonstrate secure socket programming and cryptographic primitives. Lacks identity signing features required for production-grade protection against active Man-in-the-Middle (MITM) attacks.

📄 License

Open-source project for educational use.
