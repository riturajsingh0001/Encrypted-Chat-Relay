🔒 End-to-End Encrypted Chat Relay (CLI Version)
A Secure, Multi-Threaded Peer-to-Peer Messaging System Built in Python

This project demonstrates how modern secure messengers implement true End-to-End Encryption (E2EE) using Ephemeral Elliptic Curve Diffie-Hellman (ECDH), HKDF key derivation, and AES-256-GCM authenticated encryption, while the server remains completely blind to message content.

🚀 Features
🔐 True End-to-End Encryption

Messages are encrypted before leaving the client.
The relay server receives only encrypted bytes.

🔄 Perfect Forward Secrecy

Each session uses fresh Ephemeral ECDH (SECP256R1) keys.
Even if a session key leaks, all past messages remain protected.

🛡️ Authenticated Encryption (AES-256-GCM)

AES-GCM provides:

Confidentiality

Integrity

Tamper detection

🛰️ Blind Relay Server

Server acts only as a dumb pipe:

No decryption

No key storage

No message inspection

🧵 Multi-Threaded Client

Real-time encrypted chat with separate threads for:

Sending messages

Receiving messages

🧰 Technology Stack
Component	Technology
Language	Python 3
Networking	socket, threading
Key Exchange	ECDH (SECP256R1)
KDF	HKDF (SHA-256)
Encryption	AES-256-GCM
Library	cryptography (hazmat)
⚙️ How to Run (CLI Mode)

This system includes:

1 Relay Server

2 or more Encrypted Clients

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


Handshake will automatically complete:

[SUCCESS] Secure Channel Established!

5️⃣ Start Secure Chatting
Alice > hello bob 👋
Bob   > encrypted message received 🔐


Encrypted messages flow securely through the relay server.

6️⃣ Stop the System

Stop client:

/exit


Stop server:

CTRL + C

📌 Example CLI Session
$ python secure_server.py --host 0.0.0.0 --port 5000
[SERVER] Relay started on 0.0.0.0:5000

$ python secure_client.py --host 127.0.0.1 --port 5000 --name Alice
[CLIENT] Generating ECDH keys...
[CLIENT] Exchanging public keys...
[SUCCESS] Secure Channel Established!

$ python secure_client.py --host 127.0.0.1 --port 5000 --name Bob
[SUCCESS] Secure Channel Established!

Alice > hey bob!
Bob   > hi alice, encrypted message received!

🔐 Security Architecture
1️⃣ Ephemeral ECDH Key Exchange

Each client generates:

A fresh ECC private key

A public key to share through the server

Both sides compute:

shared_secret = ECDH(private_self, public_peer)

2️⃣ HKDF Key Derivation

Shared secret is expanded into a strong AES key:

HKDF(SHA-256) → 256-bit session key

3️⃣ AES-256-GCM Encryption

For every message:

Generate a unique random nonce

Encrypt with AES-GCM

Send nonce + ciphertext + tag

Recipient verifies integrity and decrypts

4️⃣ Blind Relay Architecture

Server only forwards bytes.
It cannot:

Decrypt

Modify

Read

Analyze

This ensures full end-to-end privacy.

⚠️ Disclaimer

This project is intended for educational and research purposes.
It lacks:

Identity key verification

MITM protection

Long-term key management

For real-world secure messengers, protocols like:

X3DH

Double Ratchet (Signal Protocol)
are required.

🤝 Contributing

We welcome contributions!
Follow the standard GitHub flow:

1. Create a new branch:
git checkout -b feature/YourFeature

2. Commit your changes:
git commit -m "Add your feature"

3. Push your branch:
git push origin feature/YourFeature

4. Open a pull request to the main branch.
📄 License

This project is open-source and free to use for learning, research, and experimentation.
