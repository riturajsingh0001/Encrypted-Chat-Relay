🔒 End-to-End Encrypted Chat Relay
A Secure, Multi-Threaded P2P Messaging System in Python

A lightweight yet powerful demonstration of true End-to-end Encryption (E2EE) implemented from scratch using Elliptic Curve Cryptography, AES-GCM, and secure socket communication.
This project shows how modern encrypted messengers derive keys, encrypt messages, and relay ciphertext safely—even through an untrusted server.

🚀 Key Features
🔐 True End-to-End Encryption (E2EE)

All messages are encrypted locally before leaving the client device.
The relay server receives only random-looking ciphertext, ensuring complete privacy.

🔄 Perfect Forward Secrecy (PFS)

Each session uses fresh Ephemeral ECDH (SECP256R1) keys.
Even if a key is compromised, past conversations remain protected.

🛡️ Authenticated Encryption

Powered by AES-256-GCM, ensuring:

Confidentiality

Integrity

Tamper detection

Any modification to ciphertext instantly invalidates the message.

🧵 Multi-threaded Architecture

Separate threads handle:

Sending messages

Receiving messages

…giving a smooth, real-time chat experience.

🛰️ Blind Relay Server

The server acts purely as a dumb pipe:

No decryption

No key storage

No message inspection
Exactly how a secure messenger should behave.

🧰 Technology Stack
Component	Technology
Language	Python 3
Networking	socket, threading
Cryptography	cryptography (hazmat primitives)
Key Exchange	ECDH (SECP256R1)
Key Derivation	HKDF (SHA-256)
Encryption	AES-256-GCM (256-bit)
📦 Prerequisites

Install dependencies:

pip install cryptography


Requires Python 3.8+.

⚙️ Running the Project

This system uses:

1 server (relay)

2 or more clients

1️⃣ Start the Server
python secure_server.py


It will begin listening for incoming client connections.

2️⃣ Start Client A
python secure_client.py

3️⃣ Start Client B
python secure_client.py


Once both clients are connected, the ECDH handshake happens automatically.
You will see:

[SUCCESS] Secure Channel Established!


You can now chat privately and securely!

🔐 Security Architecture (Deep Dive)
1. Initial Client Connection

Each client connects to the relay server via TCP.

2. Ephemeral ECDH Handshake

Each client generates:

An ephemeral ECC private key

A matching public key

Public keys are exchanged through the server (server cannot decrypt anything).

Both clients compute:

Shared Secret = ECDH(PrivateKey_self, PublicKey_peer)

3. HKDF Key Derivation

The shared secret is transformed into a strong AES key using:

HKDF(SHA-256) → 256-bit AES Session Key

4. Secure Transport

For every message:

A unique nonce (IV) is generated.

Message is encrypted with AES-256-GCM.

Ciphertext + nonce + auth-tag are sent to the server.

Server broadcasts them as raw bytes.

Recipient:

Verifies integrity using GCM tag

Decrypts the plaintext

This ensures privacy, authenticity, and tamper detection.

⚠️ Disclaimer

This project is built for educational and research purposes.
Although it uses industry-standard cryptographic algorithms, it lacks:

Identity verification

Public key signatures

Certificate pinning

Therefore, it is not safe against MITM attacks during the handshake.
For production-grade messengers, implement signed keys / X3DH / Double Ratchet.

📄 License

This project is open-source.
Feel free to modify, extend, or integrate it into your own applications.
