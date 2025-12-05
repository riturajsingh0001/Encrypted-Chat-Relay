🔒 End-to-End Encrypted Chat Relay (CLI Version)

A Secure, Multi-Threaded Peer-to-Peer Messaging System Built in Python

This project demonstrates how secure messengers implement true End-to-End Encryption (E2EE) using Ephemeral ECDH, HKDF, and AES-256-GCM, while the relay server remains completely blind to message content.

🚀 Features
🔐 True End-to-End Encryption

Messages are encrypted before leaving the client.
The server handles only ciphertext.

🔄 Perfect Forward Secrecy

Fresh Ephemeral ECDH (SECP256R1) keys for every session.

🛡 AES-256-GCM Authenticated Encryption

Confidentiality + Integrity + Tamper detection.

🛰 Blind Relay Server

Server cannot decrypt or inspect anything.

🧵 Multi-threaded Client

Handles sending + receiving simultaneously.

🧰 Technology Stack
Component	Tech
Language	Python 3
Networking	socket, threading
ECC Key Exchange	SECP256R1
KDF	HKDF (SHA-256)
Encryption	AES-256-GCM
Crypto Library	cryptography
⚙️ How to Run (CLI Mode)

This application runs using:

1 Relay Server

2 or more Encrypted Clients

Below is the fully fixed version — all commands are in proper GitHub code blocks.

1️⃣ Install Dependencies
pip install cryptography

2️⃣ Start the Relay Server
python secure_server.py --host 0.0.0.0 --port 5000


Verbose mode:

python secure_server.py --host 0.0.0.0 --port 5000 --verbose


Expected output:

[SERVER] Relay started on 0.0.0.0:5000

3️⃣ Start Client A

Open a new terminal:

python secure_client.py --host 127.0.0.1 --port 5000 --name Alice

4️⃣ Start Client B

Open another terminal:

python secure_client.py --host 127.0.0.1 --port 5000 --name Bob


Handshake automatically completes:

[SUCCESS] Secure Channel Established!

5️⃣ Start Secure Chatting
Alice > hello bob 👋
Bob   > encrypted message received 🔐


Encrypted messages flow securely through the relay server.

6️⃣ Stop the System

Stop client:

/exit


🔐 Security Architecture
1️⃣ Ephemeral ECDH Key Exchange

Each client generates:

ECC private key

ECC public key

Then computes:

shared_secret = ECDH(private_self, public_peer)

2️⃣ HKDF Key Derivation
HKDF(SHA-256) → 256-bit AES session key

3️⃣ AES-256-GCM Encryption

For each message:

Generate random nonce

Encrypt using AES-GCM

Send (nonce + ciphertext + tag)

Receiver verifies and decrypts

4️⃣ Blind Relay Architecture

Server is unable to:

Read messages

Modify messages

Analyze content

Reconstruct keys

⚠️ Disclaimer

This project is for learning and research.
It does not include:

Identity verification

MITM protection

Long-term key management

For production security, protocols like X3DH and Double Ratchet are required.



Stop server:

CTRL + C
